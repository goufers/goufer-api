# API Documentation

## Overview

This documentation covers the following API endpoints:
1. User Login
2. User Signup
3. Send Code
3. Verify Phone
5. Search for Gofers
6. Get all available Gofers
7. Get single Gofer profile information
8. Password Reset
9. Toggle Availability for Gofers
10. Logged in User Profile

## Endpoints

### 1. User Login

#### Endpoint
```
POST /api/v1/users/login/
```

#### Description
This endpoint allows users to log in by providing their email or phone number and password. Upon successful authentication, a pair of JWT tokens (access and refresh) is returned, which can be used for authorized access to other endpoints.

#### Request
##### Headers
- `Content-Type: application/json`

##### Body
```json
{
    "identifier": "string",  // Either email or phone number
    "password": "string"
}
```

#### Response
##### Success (200 OK)
```json
{
    "refresh": "string",
    "access": "string"
}
```

##### Error (401 Unauthorized)
```json
{
    "detail": "Invalid credentials"
}
```

### 2. User Signup

#### Endpoint
```
POST /api/v1/users/register/
```

#### Description
This endpoint allows new users to create an account by providing necessary details like email, password, and phone number. Upon successful registration, a pair of JWT tokens (access and refresh) is returned.

#### Request
##### Headers
- `Content-Type: application/json`

##### Body
```json
{
    "email": "string",
    "phone_number": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}
```

#### Response
##### Success (201 Created)
```json
{
    "refresh": "string",
    "access": "string",
    "email": "string",
    "phone_number": "string",
}
```

##### Error (400 Bad Request)
```json
{
    "detail": "Detailed error message"
}
```

### 3. Send Code

#### Endpoint
```
POST /api/v1/users/send-code/
```

#### Description
This endpoint is used to send a code to a user's phone number

#### Request
##### Headers
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

##### Body
```json
{
    "phone_number": "phone number"
}
```

#### Response
##### Success (200 OK)
```json
{
    "detail": "Verification code sent successfully."
}
```

### 4. Verify Phone

#### Endpoint
```
POST /api/v1/users/verify-phone/
```

#### Description
This endpoint is used to verify the user's phone number. The user should provide the verification code sent to their phone number.

#### Request
##### Headers
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

##### Body
```json
{
    "code": "string"
}
```

#### Response
##### Success (200 OK)
```json
{
    "detail": "Phone number verified successfully."
}
```

##### Error (400 Bad Request)
```json
{
    "detail": "Invalid or expired verification code."
}
```

### 5. Search for Gofers

#### Endpoint

```
GET /api/v1/users/gofers?search=keyword
```

#### Description

Keyword Searches for matching Gofers using Location, mobility means and expertise

#### Example Request

```
GET /api/v1/users/gofers/?search=necklaces
```

#### Example Response

> List of Matching Gofer Objects if a match is found

```json
[
    {
        "id": 3,
        "documents": [],
        "expertise": "TEFL teacher",
        "mobility_means": "Motorcycle",
        "bio": "Accept my hot center education strong sing. Everybody wall herself him place successful.\nDeal writer his subject lose. Agent himself party media six popular late.\nTrial sometimes ten.",
        "charges": 898,
        "custom_user": 3,
        "sub_category": 17,
        "location": 11
    },
    {
        "id": 5,
        "documents": [],
        "expertise": "Make",
        "mobility_means": "Motorcycle",
        "bio": "City water page so sort. Professor work trade clearly almost value our. Of take baby great explain.\nGun concern phone central person hold surface quite. American project big simply.",
        "charges": 349,
        "custom_user": 5,
        "sub_category": 2,
        "location": 19
    }
]
```

## Other Features

### A. Filtering of Gofers

#### Endpoint

```
GET /api/v1/gofers?filter_options
```

#### Description

> Show a list of Gofers that match only a set of filter options


### Filters
You can use the following query parameters to filter gofers:

- `category`: Filter by category name (partial match, case-insensitive).
- `state`: Filter by gofer's state (partial match, case-insensitive).
- `country`: Filter by gofer's country (partial match, case-insensitive).
- `expertise`: Filter by expertise (partial match, case-insensitive).
- `charges_above`: Filter by charges greater than the specified value.
- `charges_below`: Filter by charges less than the specified value.
- `avg_rating`: Filter by minimum rating
- `gender`: Filter by gender ('M' for Male, 'F' for Female).

### Sorting
You can sort the results using the `ordering` parameter. Use `ordering=field_name` for ascending order or `ordering=-field_name` for descending order. Supported fields: `mobility_means`, `charges`, `avg_rating`.

### Example Requests and Responses

#### Filter by Sub-Category and Country
##### Request
```
GET /api/v1/users/gofers/?sub_category=Fashion and Beauty&country=Bahamas
```
##### Response
```json
[
{
    "id": 12,
    "sub_category": {
      "id": 21,
      "name": "Difficult",
      "description": "Leader service without step manage boy. Perhaps too morning look word.\nBuy news expert free amount religious. Because guess board society end."
    },
    "custom_user": {
      "email": "nsmith@example.net",
      "phone_number": "001-310-664-8809x8617",
      "first_name": "",
      "last_name": "",
      "gender": "O",
      "location": 15,
      "address": {
        "id": 4,
        "house_number": "416",
        "street": "Brown Crossing",
        "city": "West Angelafurt",
        "state": "Arizona",
        "country": "Bahamas"
      },
      "documents": [],
      "phone_verified": true,
      "email_verified": false
    },
    "gofer_reviews": [],
    "expertise": "Armed forces technical officer",
    "mobility_means": "Motorcycle",
    "bio": "Mission few big with whose. Behind up contain lead plant rate.\nShoulder gas town reason. Beyond daughter administration fall sign.",
    "charges": 510,
    "is_available": false,
    "avg_rating": 0.0
  }
]
```

#### Filter by Sub-Category
##### Request
```
GET /api/v1/users/gofers/?category=Entertainment
```
##### Response
```json
[
  {
    "id": 15,
    "sub_category": {
      "id": 29,
      "name": "Floor",
      "description": "Phone remember second identify owner. Own research best major ago."
    },
    "custom_user": {
      "email": "parkerchristopher@example.com",
      "phone_number": "+1-445-816-8787",
      "first_name": "",
      "last_name": "",
      "gender": "M",
      "location": 2,
      "address": {
        "id": 14,
        "house_number": "73059",
        "street": "Gutierrez Mountain",
        "city": "East Davidport",
        "state": "Hawaii",
        "country": "Afghanistan"
      },
      "documents": [],
      "phone_verified": false,
      "email_verified": false
    },
    "gofer_reviews": [],
    "expertise": "Designer, jewellery",
    "mobility_means": "Car",
    "bio": "Modern growth concern. Make join window vote street. Tonight lead remain administration almost social. Sell year join reduce Mrs son answer in.",
    "charges": 346,
    "is_available": false,
    "avg_rating": 0.0
  }
]
```

#### Filter by State
##### Request
```
GET /api/v1/users/gofers/?state=Arizona
```
##### Response
```json
[
  {
    "id": 12,
    "sub_category": {
      "id": 21,
      "name": "Difficult",
      "description": "Leader service without step manage boy. Perhaps too morning look word.\nBuy news expert free amount religious. Because guess board society end."
    },
    "custom_user": {
      "email": "nsmith@example.net",
      "phone_number": "001-310-664-8809x8617",
      "first_name": "",
      "last_name": "",
      "gender": "O",
      "location": 15,
      "address": {
        "id": 4,
        "house_number": "416",
        "street": "Brown Crossing",
        "city": "West Angelafurt",
        "state": "Arizona",
        "country": "Bahamas"
      },
      "documents": [],
      "phone_verified": true,
      "email_verified": false
    },
    "gofer_reviews": [],
    "expertise": "Armed forces technical officer",
    "mobility_means": "Motorcycle",
    "bio": "Mission few big with whose. Behind up contain lead plant rate.\nShoulder gas town reason. Beyond daughter administration fall sign.",
    "charges": 510,
    "is_available": false,
    "avg_rating": 0.0
  }
]
```

#### Filter by Country
##### Request
```
GET /api/v1/users/gofers/?country=Nigeria
```
##### Response
```json
[
  {
    "id": 1,
    "sub_category": {
      "id": 4,
      "name": "Bank",
      "description": "Investment this idea might really. Talk word life necessary price. Second idea democratic site certain including. Single message full west democratic."
    },
    "custom_user": {
      "email": "jamieyork@example.com",
      "phone_number": "5856464523",
      "first_name": "",
      "last_name": "",
      "gender": "O",
      "location": 12,
      "address": {
        "id": 13,
        "house_number": "369",
        "street": "Hernandez Spurs",
        "city": "Laurenshire",
        "state": "Rhode Island",
        "country": "Fiji"
      },
      "documents": [],
      "phone_verified": true,
      "email_verified": false
    },
    "gofer_reviews": [],
    "expertise": "Fine artist",
    "mobility_means": "Bicycle",
    "bio": "Girl election soldier movement finish soldier industry.\nOld relate cause. In her miss employee reason.\nLearn science once almost society event outside customer. Account member fear tonight.",
    "charges": 524,
    "is_available": false,
    "avg_rating": 0.0
  }
]
```

#### Filter by Expertise
##### Request
```
GET /api/v1/users/gofers/?expertise=Ophthalmology
```
##### Response
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        "sub_category": "eye",
        "expertise": "Ophthalmology",
        "mobility_means": "Car",
        "charges": 200.0,
        "location": {
            "city": "Nairobi",
            "state": "Nairobi",
            "country": "Kenya"
        },
        "bio": "Experienced ophthalmologist with over 10 years in practice."
    }
]
```


#### Filter by High Charges
##### Request
```
GET /api/v1/users/gofers/?charges_above=100
```
##### Response
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        "sub_category": "eye",
        "expertise": "Ophthalmology",
        "mobility_means": "Car",
        "charges": 200.0,
        "location": {
            "city": "Nairobi",
            "state": "Nairobi",
            "country": "Kenya"
        },
        "bio": "Experienced ophthalmologist with over 10 years in practice."
    }
]
```

#### Filter by Low Charges
##### Request
``>
GET /api/v1/users/gofers/?charges_below=300
```
##### Response
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        "sub_category": "eye",
        "expertise": "Ophthalmology",
        "mobility_means": "Car",
        "charges": 200.0,
        "location": {
            "city": "Nairobi",
            "state": "Nairobi",
            "country": "Kenya"
        },
        "bio": "Experienced ophthalmologist with over 10 years in practice."
    }
]
```


#### Filter by Gender

**Request:**
```
GET /api/v1/users/gofers/?gender=F
```

**Response:**
```json
[
    {
        "id": 3,
        "custom_user": 3,
        "sub_category": {
            "id": 7,
            "name": "Education",
            "description": "Education description..."
        },
        "location": {
            "id": 3,
            "latitude": 40.123456,
            "longitude": 120.123456,
            "address": "5678 Teacher St\nSomecity, CA 12345",
            "state": "California",
            "country": "USA"
        },
        "expertise": "Teacher",
        "mobility_means": "Bicycle",
        "bio": "Teaching professional...",
        "charges": 200,
        "is_available": true,
        "rating": 4.7
    }
]
```

#### Filter by Average Rating

**Request:**
```
GET /api/v1/users/gofers/?avg_rating=4.5
```

**Response:**
```json
[
    {
        "id": 6,
        "custom_user": 6,
        "sub_category": {
            "id": 10,
            "name": "Music",
            "description": "Music description..."
        },
        "location": {
            "id": 6,
            "latitude": 38.123456,
            "longitude": 108.123456,
            "address": "1234 Music St\nSomecity, IL 12345",
            "state": "Illinois",
            "country": "USA"
        },
        "expertise": "Musician",
        "mobility_means": "Car",
        "bio": "Music professional...",
        "charges": 350,
        "is_available": true,
        "rating": 4.8
    }
]
```

#### Filter by Availability (presence)

**Request:**
```
GET /api/v1/users/gofers/?is_available=true
```

**Response:**
```json
[
    {
        "id": 7,
        "custom_user": 7,
        "sub_category": {
            "id": 11,
            "name": "Finance",
            "description": "Finance description..."
        },
        "location": {
            "id": 7,
            "latitude": 37.123456,
            "longitude": 107.123456,
            "address": "8765 Finance St\nSomecity, CO 12345",
            "state": "Colorado",
            "country": "USA"
        },
        "expertise": "Accountant",
        "mobility_means": "Motorcycle",
        "bio": "Finance professional...",
        "charges": 300,
        "is_available": true,
        "rating": 4.4
    }
]
```

### Combining Filters

You can combine multiple filters in a single request.

**Request:**
```
GET /api/v1/users/gofers/?sub_category=tech&location=New&gender=M&charges_above=300&avg_rating=4.5&is_available=true
```

**Response:**
```json
[
    {
        "id": 8,
        "custom_user": 8,
        "sub_category": {
            "id": 12,
            "name": "Technology",
            "description": "Technology description..."
        },
        "location": {
            "id": 8,
            "latitude": 36.123456,
            "longitude": 106.123456,
            "address": "5432 Tech St\nSomecity, NY 12345",
            "state": "New York",
            "country": "USA"
        },
        "expertise": "Data Scientist",
        "mobility_means": "Car",
        "bio": "Data professional...",
        "charges": 450,
        "is_available": true,
        "rating": 4.9
    }
]
```

### Sorting Example
##### Request
    GET /api/v1/users/gofers/?sub_category=eye&location=Ken&ordering=charges

##### Response
```json
[
    {
        "id": 2,
        "user": {
            "id": 2,
            "username": "jane_doe",
            "email": "jane@example.com"
        },
        "sub_category": "eye",
        "expertise": "Ophthalmology",
        "mobility_means": "Bike",
        "charges": 150.0,
        "location": {
            "city": "Mombasa",
            "state": "Mombasa",
            "country": "Kenya"
        },
        "bio": "Ophthalmologist specializing in pediatric eye care."
    },
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        "sub_category": "eye",
        "expertise": "Ophthalmology",
        "mobility_means": "Car",
        "charges": 200.0,
        "location": {
            "city": "Nairobi",
            "state": "Nairobi",
            "country": "Kenya"
        },
        "bio": "Experienced ophthalmologist with over 10 years in practice."
    }
]
```


### 6. Get all available Gofers

#### Endpoint

```
GET /api/v1/users/gofers/
```

#### Example Response

```json
[
    {
  "id": 1,
  "documents": [],
  "sub_category": {
    "id": 5,
    "name": "Military",
    "description": "Trial state what major energy race improve. Thus executive top lawyer just lay. Detail participant cover then nice become party skin.\nHope many finally listen."
  },
  "location": {
    "id": 1,
    "latitude": 49.331095,
    "longitude": 107.534661,
    "address": "5645 Glenn Divide Apt. 738\nLake Michaelfort, ME 69113",
    "state": "North Dakota",
    "country": "Algeria"
  },
  "avg_rating": null,
  "expertise": "Orthoptist",
  "mobility_means": "Bicycle",
  "bio": "Or sure five benefit success nice sure. Then common figure local.\nOften network image important animal gas husband. True everything fill right wait floor three look. Do of community citizen.",
  "charges": 250,
  "custom_user": 1
}

]
```

### 7. Get single Gofer profile information

#### Endpoint

```
GET /api/v1/users/gofers/<gofer_id>
```

#### Example Response

```json
{
  "id": 1,
  "documents": [],
  "sub_category": {
    "id": 5,
    "name": "Military",
    "description": "Trial state what major energy race improve. Thus executive top lawyer just lay. Detail participant cover then nice become party skin.\nHope many finally listen."
  },
  "location": {
    "id": 1,
    "latitude": 49.331095,
    "longitude": 107.534661,
    "address": "5645 Glenn Divide Apt. 738\nLake Michaelfort, ME 69113",
    "state": "North Dakota",
    "country": "Algeria"
  },
  "custom_user": {
    "gender": "F",
    "first_name": "",
    "last_name": "",
    "location": {
      "id": 1,
      "latitude": 49.331095,
      "longitude": 107.534661,
      "address": "5645 Glenn Divide Apt. 738\nLake Michaelfort, ME 69113",
      "state": "North Dakota",
      "country": "Algeria"
    }
  },
  "expertise": "Orthoptist",
  "mobility_means": "Bicycle",
  "bio": "Or sure five benefit success nice sure. Then common figure local.\nOften network image important animal gas husband. True everything fill right wait floor three look. Do of community citizen.",
  "charges": 250,
  "is_available": true,
  "avg_rating": 3.5
}
```

### 8. Password Reset

### Description

    Endpoint to enable users to reset their password.
    Password Reset link is sent to the Logged in user's email.

#### Endpoint


### 9. Toggle Availability

This API endpoint allows a logged-in Gofer to toggle their availability status.

#### Endpoint

`POST /api/v1/toggle-available/`

#### Authentication

- **Required**: Yes
- **Method**: Bearer Token

#### Permissions

- **Required**: IsAuthenticated

#### Request Headers

- **Authorization**: `Bearer <your_token_here>`

#### Request Body

- **Required**: None

#### Response

- **Success (200 OK)**:
    - Returns the updated Gofer object with the new availability status.
    - **Example**:
    ```json
    {
        "id": 1,
        "custom_user": 1,
        "expertise": "Orthoptist",
        "mobility_means": "Bicycle",
        "bio": "Or sure five benefit success nice sure...",
        "sub_category": {
            "id": 5,
            "name": "Military",
            "description": "Trial state what major energy race improve..."
        },
        "location": {
            "id": 1,
            "latitude": 49.331095,
            "longitude": 107.534661,
            "address": "5645 Glenn Divide Apt. 738\nLake Michaelfort, ME 69113",
            "state": "North Dakota",
            "country": "Algeria"
        },
        "rating": null,
        "charges": 250,
        "is_available": true
    }
    ```
- **Error (400 Bad Request)**:
    - **Example**:
    ```json
    {
        "error": "This user is not a Gofer"
    }
    ```

#### Example Request

```
POST /api/v1/toggle-available/
Authorization: Bearer <your_token_here>
Content-Type: application/json
```

#### Example Response

- **Success**:
```json
{
  "id": 51,
  "sub_category": {
    "id": 12,
    "name": "Consumer",
    "description": "Just thing skill. Maintain thousand market.\nSafe project lay particularly end throw activity. Door stand reflect she."
  },
  "custom_user": {
    "id": 52,
    "email": "ezekielokebule11011@outlook.com",
    "phone_number": "+2348125342305",
    "first_name": "Jonathan",
    "last_name": "Hughes",
    "gender": "M",
    "location": null,
    "address": null,
    "documents": [],
    "date_joined": "2024-07-04T08:47:43.545528Z",
    "phone_verified": false,
    "email_verified": false
  },
  "gofer_reviews": [],
  "gofer_media": [],
  "expertise": "I sell and buy stolen bikes",
  "mobility_means": "Bicycle",
  "bio": "I love you\r\nI love you\r\nI love you\r\nI love you",
  "charges": 900,
  "is_available": false,
  "avg_rating": 0.0
}
```
---
