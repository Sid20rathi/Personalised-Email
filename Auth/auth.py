from fastapi import HTTPException ,status, Depends ,requests
from clerk_backend_api import Clerk ,AuthenticateRequestOptions

import os 
from dotenv import load_dotenv
load_dotenv()


clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


def authenticate_and_get_user(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties =["http://localhost:3000"],
                jwt_key=os.getenv("JWT_TOKEN"),
            )

        )

        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
               
                )

        user_id = request_state.payload.get("sub")

        return {"user_id":user_id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error:{e}",
       
            )

