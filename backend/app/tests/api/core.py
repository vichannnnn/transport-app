from app import schemas
from fastapi.testclient import TestClient
from fastapi import status
from fastapi.encoders import jsonable_encoder

STATION_URL = "/station"
CONNECTING_STATION_URL = "/connecting_station"
ALL_STATIONS_URL = "/all_stations"


def test_station_post_endpoint(test_client: TestClient, train_station: schemas.core.TrainStationSchema):
    payload = jsonable_encoder(train_station)
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK

    resp_data = response.json()
    assert resp_data['id'] == train_station.id
    assert resp_data['name'] == train_station.name
    assert resp_data['interchange'] == train_station.interchange


def test_station_get_endpoint(test_client: TestClient):
    params = {'name': 'Buona Vista'}
    response = test_client.get(STATION_URL, params=params)
    assert response.status_code == status.HTTP_200_OK


def test_no_duplicate_station(test_client: TestClient, train_station_2: schemas.core.TrainStationSchema):
    payload = jsonable_encoder(train_station_2)
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.post(STATION_URL, json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


