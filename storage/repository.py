from storage.database import SessionLocal
from storage.models import TestRun


class RunRepository:

    def save(self, data):

        db = SessionLocal()

        try:

            run = TestRun(**data)

            db.add(run)

            db.commit()

            db.refresh(run)

            return run

        finally:

            db.close()

    def latest(self):

        db = SessionLocal()

        try:

            return (
                db.query(TestRun)
                .order_by(TestRun.id.desc())
                .first()
            )

        finally:

            db.close()

    def history(self, limit=100):

        db = SessionLocal()

        try:

            rows = (
                db.query(TestRun)
                .order_by(TestRun.id.desc())
                .limit(limit)
                .all()
            )

            return list(reversed(rows))

        finally:

            db.close()

    def latest_by_location(
        self,
        location
    ):

        db = SessionLocal()

        try:

            return (
                db.query(TestRun)
                .filter(
                    TestRun.location == location
                )
                .order_by(TestRun.id.desc())
                .first()
            )

        finally:

            db.close()

    def history_by_location(
        self,
        location,
        limit=100
    ):

        db = SessionLocal()

        try:

            rows = (
                db.query(TestRun)
                .filter(
                    TestRun.location == location
                )
                .order_by(TestRun.id.desc())
                .limit(limit)
                .all()
            )

            return list(reversed(rows))

        finally:

            db.close()

    def available_locations(self):

        db = SessionLocal()

        try:

            rows = (
                db.query(
                    TestRun.location
                )
                .distinct()
                .all()
            )

            return [
                r[0]
                for r in rows
                if r[0]
            ]

        finally:

            db.close()