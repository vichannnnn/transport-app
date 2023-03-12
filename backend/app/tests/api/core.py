from app import schemas
from fastapi.testclient import TestClient
from fastapi import status
from fastapi.encoders import jsonable_encoder

STATION_URL = "/station"
CONNECTING_STATION_URL = "/connecting_station"
ALL_STATIONS_URL = "/all_stations"


def test_station_post_endpoint(
    test_client: TestClient, train_station: schemas.core.TrainStationSchema
):
    payload = jsonable_encoder(train_station)
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK

    resp_data = response.json()
    assert resp_data["id"] == train_station.id
    assert resp_data["name"] == train_station.name
    assert resp_data["interchange"] == train_station.interchange


def test_station_get_endpoint(
    test_client: TestClient, train_station: schemas.core.TrainStationSchema
):
    params = {"name": train_station.name}
    response = test_client.get(STATION_URL, params=params)
    resp_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert resp_data["id"] == train_station.id
    assert resp_data["name"] == train_station.name
    assert resp_data["interchange"] == train_station.interchange


def test_no_duplicate_station_and_update_endpoint(
    test_client: TestClient,
    station_to_be_replaced: schemas.core.TrainStationSchema,
    train_station_2: schemas.core.TrainStationSchema,
):
    payload = jsonable_encoder(station_to_be_replaced)
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK

    resp_data = response.json()
    assert resp_data["id"] == station_to_be_replaced.id
    assert resp_data["name"] == station_to_be_replaced.name
    assert resp_data["interchange"] == station_to_be_replaced.interchange
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

    payload = jsonable_encoder(train_station_2)
    params = {"id": station_to_be_replaced.id}
    response = test_client.put(STATION_URL, json=payload, params=params)
    assert response.status_code == status.HTTP_200_OK

    resp_data = response.json()
    assert resp_data["id"] == train_station_2.id
    assert resp_data["name"] == train_station_2.name
    assert resp_data["interchange"] == train_station_2.interchange


def test_connecting_station_post_endpoint(
    test_client: TestClient,
    connecting_station: schemas.core.ConnectingStationSchema,
    connecting_station_2: schemas.core.ConnectingStationSchema,
):
    payload = jsonable_encoder(connecting_station)
    response = test_client.post(CONNECTING_STATION_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
