from fastapi import HTTPException, status

from api.ports.outbound.test_suite_repository import TestSuiteRepository


async def delete_suite(suite_id: str, repo: TestSuiteRepository) -> None:
    deleted = await repo.delete(suite_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")
