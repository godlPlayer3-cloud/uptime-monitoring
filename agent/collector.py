import os
import time

from datetime import datetime
from playwright.sync_api import sync_playwright

from agent.config import LOCATION


def collect(url):

    os.makedirs(
        "screenshots",
        exist_ok=True
    )

    screenshot_file = (
        f"screenshots/"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 720
            }
        )

        #
        # Inject CLS observer BEFORE navigation
        #
        page.add_init_script("""
            window.__cls = 0;
            try {
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            window.__cls += entry.value;
                        }
                    }
                }).observe({ type: 'layout-shift', buffered: true });
            } catch(e) {}
        """)

        total_bytes = 0
        request_count = 0

        def on_response(response):

            nonlocal total_bytes
            nonlocal request_count

            request_count += 1

            try:

                size = response.headers.get(
                    "content-length"
                )

                if size:
                    total_bytes += int(size)

            except Exception:
                pass

        page.on(
            "response",
            on_response
        )

        #
        # USER READY TIMER START
        #
        start_time = time.time()

        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_selector(
            "body",
            timeout=30000
        )

        #
        # Allow React / SPA rendering
        #
        page.wait_for_timeout(5000)

        #
        # User ready time
        #
        qr_ready_time = round(
            time.time() - start_time,
            2
        )

        print(
            "Title:",
            page.title()
        )

        print(
            "URL:",
            page.evaluate(
                "() => location.href"
            )
        )

        print(
            "Images:",
            page.evaluate(
                "() => document.images.length"
            )
        )

        #
        # Navigation Metrics
        #
        nav = page.evaluate(
            """
            () => {

                const n =
                  performance.getEntriesByType(
                    'navigation'
                  )[0];

                return {

                    dns:
                      n.domainLookupEnd -
                      n.domainLookupStart,

                    tcp:
                      n.connectEnd -
                      n.connectStart,

                    tls:
                      n.secureConnectionStart > 0
                        ? n.connectEnd -
                          n.secureConnectionStart
                        : 0,

                    ttfb:
                      n.responseStart -
                      n.requestStart,

                    load:
                      Math.max(
                        n.duration || 0,
                        n.domComplete || 0
                      )
                };
            }
            """
        )

        #
        # Core Web Vitals
        #
        web_vitals = page.evaluate(
            """
            () => {

                const nav =
                  performance.getEntriesByType(
                    'navigation'
                  )[0];

                // LCP via PerformanceObserver entries
                const lcpEntries =
                  performance.getEntriesByType(
                    'largest-contentful-paint'
                  );

                const lcp = lcpEntries.length
                  ? lcpEntries[
                      lcpEntries.length - 1
                    ].startTime
                  : (nav ? nav.loadEventEnd : 0);

                // FCP via paint entries
                const fcpEntry =
                  performance.getEntriesByName(
                    'first-contentful-paint'
                  )[0];

                const fcp = fcpEntry
                  ? fcpEntry.startTime
                  : (nav
                      ? nav.domContentLoadedEventEnd
                      : 0);

                return {
                    fcp: fcp,
                    lcp: lcp,
                    cls: window.__cls || 0
                };
            }
            """
        )

        #
        # Screenshot
        #
        page.screenshot(
            path=screenshot_file,
            full_page=True
        )

        browser.close()

        return {

            #
            # Agent
            #
            "location":
                LOCATION,

            #
            # Availability
            #
            "status_code":
                response.status,

            #
            # Performance
            #
            "load_time":
                round(
                    max(
                        nav["load"],
                        1
                    ) / 1000,
                    2
                ),

            "qr_ready_time":
                qr_ready_time,

            #
            # Network
            #
            "ttfb":
                round(
                    nav["ttfb"],
                    2
                ),

            "dns":
                round(
                    nav["dns"],
                    2
                ),

            "tcp":
                round(
                    nav["tcp"],
                    2
                ),

            "tls":
                round(
                    nav["tls"],
                    2
                ),

            #
            # Core Web Vitals
            #
            "fcp":
                round(
                    web_vitals["fcp"] / 1000,
                    2
                ),

            "lcp":
                round(
                    web_vitals["lcp"] / 1000,
                    2
                ),

            "cls":
                round(
                    web_vitals["cls"],
                    3
                ),

            #
            # Page Metrics
            #
            "requests":
                request_count,

            "page_size":
                round(
                    total_bytes /
                    (1024 * 1024),
                    2
                ),

            #
            # Screenshot
            #
            "screenshot":
                screenshot_file
        }