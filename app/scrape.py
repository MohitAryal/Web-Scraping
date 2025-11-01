from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from urllib.parse import urljoin, urlparse
import asyncio


def get_domain(url):
    """Extract main domain"""
    return urlparse(url).netloc


def is_internal_link(link, base_url):
    """Check if link belongs to the same domain"""
    return get_domain(link) == get_domain(base_url)


async def get_first_level_links(base_url, timeout=30, wait_for_load=2, headless=True):
    """
    Fetch the provided homepage and extract all internal links (depth 0).
    """
    links_found = set()

    print(f"[INFO] Starting single-page crawl for links: {base_url}")
    print(f"[INFO] Timeout: {timeout}s | JS wait: {wait_for_load}s | Headless: {headless}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent=(
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()
        page.set_default_timeout(timeout * 1000)

        try:
            print(f"[INFO] Visiting: {base_url}")
            await page.goto(base_url, wait_until='networkidle', timeout=timeout * 1000)
            await asyncio.sleep(wait_for_load)

            anchors = await page.query_selector_all("a[href]")
            print(f"[INFO] Found {len(anchors)} total anchor tags.")

            for a in anchors:
                href = await a.get_attribute("href")
                if not href:
                    continue
                abs_url = urljoin(base_url, href.split("#")[0])
                if is_internal_link(abs_url, base_url):
                    links_found.add(abs_url)

            print(f"[INFO] Extracted {len(links_found)} internal links.")
        except PlaywrightTimeout:
            print(f"[WARN] Timeout while loading {base_url}")
        except Exception as e:
            print(f"[WARN] Error: {type(e).__name__}: {str(e)[:100]}")
        finally:
            await browser.close()

    return sorted(list(links_found))