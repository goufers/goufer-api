# API Documentation

## Overview

This documentation covers the following API endpoints:
1. User Login
2. User Signup
3. Send Code
3. Verify Phone

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
    "access": "string"
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

---
