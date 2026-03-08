from fastapi import HTTPException, status

from api.ports.outbound.project_repository import ProjectRepository


async def delete_project(project_id: str, repo: ProjectRepository) -> None:
    deleted = await repo.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
