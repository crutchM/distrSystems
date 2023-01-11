from fastapi import HTTPException, status


def throw_not_found(obj):
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)