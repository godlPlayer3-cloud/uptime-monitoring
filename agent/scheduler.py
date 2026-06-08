from apscheduler.schedulers.blocking import BlockingScheduler

from agent.collector import collect

from storage.repository import RunRepository
from storage.models import Base
from storage.database import engine

from agent.config import (
    TARGET_URL,
    RUN_INTERVAL_SECONDS,
    LOCATION,
    AGENT_NAME
)

# Create DB tables
Base.metadata.create_all(engine)

repo = RunRepository()


def run():

    print("\n===================================")
    print("Starting test run...")
    print("===================================")

    print(
        f"Location: {LOCATION}"
    )

    print(
        f"Agent: {AGENT_NAME}"
    )

    print("")

    for attempt in range(3):

        try:

            data = collect(
                TARGET_URL
            )

            repo.save(data)

            print(
                "\nSUCCESS\n"
            )

            print(
                f"Location      : {data['location']}"
            )

            print(
                f"Status        : {data['status_code']}"
            )

            print(
                f"Load Time     : {data['load_time']}s"
            )

            print(
                f"QR Ready Time : {data['qr_ready_time']}s"
            )

            print(
                f"TTFB          : {data['ttfb']}ms"
            )

            print(
                f"DNS           : {data['dns']}ms"
            )

            print(
                f"TCP           : {data['tcp']}ms"
            )

            print(
                f"TLS           : {data['tls']}ms"
            )

            print(
                f"FCP           : {data['fcp']}s"
            )

            print(
                f"LCP           : {data['lcp']}s"
            )

            print(
                f"CLS           : {data['cls']}"
            )

            print(
                f"Requests      : {data['requests']}"
            )

            print(
                f"Page Size     : {data['page_size']} MB"
            )

            print(
                f"Screenshot    : {data['screenshot']}"
            )

            return

        except Exception as e:

            print(
                f"Attempt {attempt + 1} failed:"
            )

            print(e)

            if attempt == 2:

                print(
                    "All attempts failed"
                )

                return


scheduler = BlockingScheduler()

scheduler.add_job(
    run,
    "interval",
    seconds=RUN_INTERVAL_SECONDS,
    max_instances=1,
    coalesce=True
)


if __name__ == "__main__":

    print(
        "\n==================================="
    )

    print(
        "PL MONITOR V5.3"
    )

    print(
        "===================================\n"
    )

    print(
        f"Location : {LOCATION}"
    )

    print(
        f"Agent    : {AGENT_NAME}"
    )

    print(
        f"URL      : {TARGET_URL}"
    )

    print(
        f"Interval : {RUN_INTERVAL_SECONDS}s"
    )

    run()

    print(
        "\nScheduler started...\n"
    )

    scheduler.start()