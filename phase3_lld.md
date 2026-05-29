## Introduction to the Automated Midpoint Negotiation Module
The automated midpoint negotiation module is designed to facilitate efficient and anonymous dispute resolution (ODR) by providing a neutral midpoint for negotiations. This module aims to assist parties in reaching a mutually acceptable agreement without requiring direct communication.

## System Architecture
The system will be built using the following components:
* **API Gateway**: Handles incoming requests and routes them to the appropriate microservice.
* **Negotiation Service**: Responsible for calculating midpoints, handling iterative negotiations, and providing concession analysis.
* **Data Storage**: Stores negotiation data, party information, and system configuration.
* **Logging Service**: Handles logging of process status tokens and internal mapped IDs.

### API Gateway
The API Gateway will be built using Next.js and will handle incoming requests from parties. It will route requests to the Negotiation Service and handle authentication and authorization.

### Negotiation Service
The Negotiation Service will be built using FastAPI and will handle the core functionality of the system, including:
* **Midpoint Calculation**: Calculates the midpoint between parties' initial offers.
* **Iterative Negotiation**: Handles iterative negotiations and calculates new midpoints based on party inputs.
* **Concession Analysis**: Provides insights into party concession history.

### Data Storage
The Data Storage layer will be built using PostgreSQL and pgvector. It will store:
* **Negotiation Data**: Stores negotiation history, party information, and system configuration.
* **Party Information**: Stores party details, including anonymous identifiers.

### Logging Service
The Logging Service will handle logging of process status tokens and internal mapped IDs. It will use a deterministic logging approach to ensure that logs are consistent and reliable.

## Database Migration Fields
The database migration fields will include:
* **Negotiation ID**: Unique identifier for each negotiation.
* **Party 1 Offer**: Initial offer from party 1.
* **Party 2 Offer**: Initial offer from party 2.
* **Midpoint**: Calculated midpoint between party 1 and party 2 offers.
* **Concession History**: Stores concession history for each party.
* **Process Status**: Stores process status tokens and internal mapped IDs.

```sql
CREATE TABLE negotiation_data (
  negotiation_id SERIAL PRIMARY KEY,
  party1_offer DECIMAL(10, 2),
  party2_offer DECIMAL(10, 2),
  midpoint DECIMAL(10, 2),
  concession_history TEXT,
  process_status TEXT
);

CREATE TABLE party_information (
  party_id SERIAL PRIMARY KEY,
  anonymous_identifier TEXT
);
```

## Input Validation Parameters
The input validation parameters will include:
* **Party 1 Offer**: Must be a valid decimal number between 0 and 100.
* **Party 2 Offer**: Must be a valid decimal number between 0 and 100.
* **Concession History**: Must be a valid JSON object.

```python
from pydantic import BaseModel, validator

class NegotiationRequest(BaseModel):
  party1_offer: float
  party2_offer: float
  concession_history: dict

  @validator('party1_offer')
  def validate_party1_offer(cls, v):
    if not 0 <= v <= 100:
      raise ValueError('Party 1 offer must be between 0 and 100')
    return v

  @validator('party2_offer')
  def validate_party2_offer(cls, v):
    if not 0 <= v <= 100:
      raise ValueError('Party 2 offer must be between 0 and 100')
    return v

  @validator('concession_history')
  def validate_concession_history(cls, v):
    if not isinstance(v, dict):
      raise ValueError('Concession history must be a valid JSON object')
    return v
```

## API Endpoints
The API endpoints will include:
* **POST /negotiate**: Calculates the midpoint between party 1 and party 2 offers.
* **GET /negotiation-history**: Retrieves the negotiation history for a given negotiation ID.
* **POST /concession**: Updates the concession history for a given negotiation ID.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class NegotiationRequest(BaseModel):
  party1_offer: float
  party2_offer: float

@app.post("/negotiate")
async def negotiate(negotiation_request: NegotiationRequest):
  # Calculate midpoint
  midpoint = (negotiation_request.party1_offer + negotiation_request.party2_offer) / 2
  return {"midpoint": midpoint}

@app.get("/negotiation-history")
async def get_negotiation_history(negotiation_id: int):
  # Retrieve negotiation history from database
  negotiation_history = retrieve_negotiation_history(negotiation_id)
  return {"negotiation_history": negotiation_history}

@app.post("/concession")
async def update_concession(negotiation_id: int, concession_history: dict):
  # Update concession history in database
  update_concession_history(negotiation_id, concession_history)
  return {"message": "Concession history updated successfully"}
```

## Request/Response Schemas
The request/response schemas will include:
* **Negotiation Request**: Includes party 1 and party 2 offers.
* **Negotiation Response**: Includes the calculated midpoint.
* **Concession Request**: Includes the concession history.
* **Concession Response**: Includes a success message.

```json
{
  "party1_offer": 50.0,
  "party2_offer": 60.0
}

{
  "midpoint": 55.0
}

{
  "concession_history": {
    "party1": [50.0, 55.0],
    "party2": [60.0, 55.0]
  }
}

{
  "message": "Concession history updated successfully"
}
```

## Regex Data Sanitization Layers
The regex data sanitization layers will include:
* **Party 1 Offer**: Must match the pattern `^\d{1,3}(\.\d{1,2})?$`.
* **Party 2 Offer**: Must match the pattern `^\d{1,3}(\.\d{1,2})?$`.
* **Concession History**: Must match the pattern `^{.*}$`.

```python
import re

def validate_party1_offer(party1_offer):
  pattern = r'^\d{1,3}(\.\d{1,2})?$'
  if not re.match(pattern, str(party1_offer)):
    raise ValueError('Party 1 offer must be a valid decimal number')

def validate_party2_offer(party2_offer):
  pattern = r'^\d{1,3}(\.\d{1,2})?$'
  if not re.match(pattern, str(party2_offer)):
    raise ValueError('Party 2 offer must be a valid decimal number')

def validate_concession_history(concession_history):
  pattern = r'^{.*}$'
  if not re.match(pattern, str(concession_history)):
    raise ValueError('Concession history must be a valid JSON object')
```

## PyTest Test Definitions
The PyTest test definitions will include:
* **Test Negotiation**: Tests the negotiation endpoint.
* **Test Concession**: Tests the concession endpoint.
* **Test Negotiation History**: Tests the negotiation history endpoint.

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_negotiation():
  response = client.post("/negotiate", json={"party1_offer": 50.0, "party2_offer": 60.0})
  assert response.status_code == 200
  assert response.json()["midpoint"] == 55.0

def test_concession():
  response = client.post("/concession", json={"concession_history": {"party1": [50.0, 55.0], "party2": [60.0, 55.0]}})
  assert response.status_code == 200
  assert response.json()["message"] == "Concession history updated successfully"

def test_negotiation_history():
  response = client.get("/negotiation-history", params={"negotiation_id": 1})
  assert response.status_code == 200
  assert response.json()["negotiation_history"] == {"party1": [50.0, 55.0], "party2": [60.0, 55.0]}
```

## AIBOM Configuration
The AIBOM configuration will include:
* **Negotiation Module**: Includes the negotiation endpoint.
* **Concession Module**: Includes the concession endpoint.
* **Negotiation History Module**: Includes the negotiation history endpoint.

```json
{
  "negotiation_module": {
    "endpoint": "/negotiate",
    "method": "POST",
    "request_schema": {
      "party1_offer": "float",
      "party2_offer": "float"
    },
    "response_schema": {
      "midpoint": "float"
    }
  },
  "concession_module": {
    "endpoint": "/concession",
    "method": "POST",
    "request_schema": {
      "concession_history": "dict"
    },
    "response_schema": {
      "message": "str"
    }
  },
  "negotiation_history_module": {
    "endpoint": "/negotiation-history",
    "method": "GET",
    "request_schema": {
      "negotiation_id": "int"
    },
    "response_schema": {
      "negotiation_history": "dict"
    }
  }
}
```

## Structural Verification AIBOM Configuration
The structural verification AIBOM configuration will include:
* **Negotiation Module**: Includes the negotiation endpoint.
* **Concession Module**: Includes the concession endpoint.
* **Negotiation History Module**: Includes the negotiation history endpoint.

```json
{
  "negotiation_module": {
    "endpoint": "/negotiate",
    "method": "POST",
    "request_schema": {
      "party1_offer": "float",
      "party2_offer": "float"
    },
    "response_schema": {
      "midpoint": "float"
    },
    "verification_schema": {
      "party1_offer": "float",
      "party2_offer": "float",
      "midpoint": "float"
    }
  },
  "concession_module": {
    "endpoint": "/concession",
    "method": "POST",
    "request_schema": {
      "concession_history": "dict"
    },
    "response_schema": {
      "message": "str"
    },
    "verification_schema": {
      "concession_history": "dict"
    }
  },
  "negotiation_history_module": {
    "endpoint": "/negotiation-history",
    "method": "GET",
    "request_schema": {
      "negotiation_id": "int"
    },
    "response_schema": {
      "negotiation_history": "dict"
    },
    "verification_schema": {
      "negotiation_id": "int",
      "negotiation_history": "dict"
    }
  }
}
```