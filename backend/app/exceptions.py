from fastapi import HTTPException, status


class AppError:

    STATION_NOT_FOUND_ERROR = HTTPException(
        status_code=404,
        detail="Station information is not found in train_station",
        headers={"WWW-Authenticate": "Bearer"},
    )

    STATION_ALREADY_EXISTS_ERROR = HTTPException(
        status_code=409,
        detail="Station name or id already exists train_station",
        headers={"WWW-Authenticate": "Bearer"},
    )

    STATION_QUERY_PARAMETERS_ERROR = HTTPException(
        status_code=400,
        detail="At least either id or name should be filled.",
        headers={"WWW-Authenticate": "Bearer"},
    )
