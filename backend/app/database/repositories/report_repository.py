from typing import Any

from bson import ObjectId

from app.database.repositories.base_repository import BaseRepository
from app.middleware.error_handler import AuthorizationError, NotFoundError
from app.models.collections import REPORTS
from app.models.report import ReportCreate, build_job_comparison_update, build_report_document
from app.schemas.report import JobComparisonResult
from app.utils.object_id import parse_object_id_or_not_found
from app.utils.text_utils import utc_now


class ReportRepository(BaseRepository):
    collection_name = REPORTS

    async def create_report(self, payload: ReportCreate) -> dict[str, Any]:
        now = utc_now()
        document = build_report_document(payload, created_at=now, updated_at=now)
        inserted_id = await self.insert_one(document)
        document["_id"] = inserted_id
        return document

    async def find_by_id_str(self, report_id: str) -> dict[str, Any] | None:
        object_id = parse_object_id_or_not_found(report_id, "Report not found.")
        return await self.find_by_id(object_id)

    async def find_by_id_for_user(self, report_id: str, user_id: str) -> dict[str, Any]:
        report = await self.find_by_id_str(report_id)
        if not report:
            raise NotFoundError("Report not found.")
        if report.get("user_id") != user_id:
            raise AuthorizationError("You do not have access to this report.")
        return report

    async def update_pdf_path(self, report_id: ObjectId | str, pdf_path: str) -> bool:
        object_id = report_id if isinstance(report_id, ObjectId) else parse_object_id_or_not_found(
            str(report_id), "Report not found."
        )
        return await self.update_by_id(
            object_id,
            {"$set": {"pdf_path": pdf_path, "updated_at": utc_now()}},
        )

    async def update_job_comparison(
        self,
        report_id: str,
        comparison: JobComparisonResult,
        pdf_path: str,
    ) -> bool:
        object_id = parse_object_id_or_not_found(report_id, "Report not found.")
        update_fields = build_job_comparison_update(comparison, pdf_path, utc_now())
        return await self.update_by_id(object_id, {"$set": update_fields})

    async def search_by_user(
        self,
        user_id: str,
        search: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {"user_id": user_id}

        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"original_filename": {"$regex": search, "$options": "i"}},
            ]

        cursor = self.collection.find(query).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def count_by_user(self, user_id: str) -> int:
        return await self.count({"user_id": user_id})

    async def get_average_score(self, user_id: str) -> float:
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$ats_scores.overall_score"}}},
        ]
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=1)
        if not results:
            return 0.0
        return round(float(results[0].get("avg_score") or 0), 2)

    async def delete_for_user(self, report_id: str, user_id: str) -> dict[str, Any]:
        report = await self.find_by_id_for_user(report_id, user_id)
        await self.delete_by_id(report["_id"])
        return report


report_repository = ReportRepository()
