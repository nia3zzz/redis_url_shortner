from fastapi import APIRouter, Request, Response
from validators.shortner_validators import CreateShortURLValidator
from pydantic import ValidationError
import string
import random
from utils.redis_client import redis_client

router = APIRouter()


# api route function for the creation the short url from a long url
@router.post("/shortner/")
async def create_short_url(request: Request, response: Response):
    # access the request body of the in the request
    req_body = await request.body()

    try:
        # validate the request body
        validated_req_body = CreateShortURLValidator(url=req_body)

    except ValidationError as e:

        response.status_code = 404
        return {
            "status": "error",
            "message": "Failed in type validation.",
            "errors": e.errors(),
        }

    try:
        # check if the url is already saved in the memory database
        check_duplicate_shortened_url = redis_client.get(validated_req_body.url)

        if check_duplicate_shortened_url != None:
            response.status_code = 409
            return {
                "status": "error",
                "message": "This url was already shortened.",
            }

        # generate the short url
        BASE62 = string.ascii_letters + string.digits

        generated_short_url = "".join(random.choices(BASE62, k=6))

        # save the generated short url along with the raw url as a key value pair
        redis_client.set(validated_req_body.url, generated_short_url)

        response.status_code = 201
        return {
            "status": "success",
            "message": "URl has been shortened.",
            "data": {"shortened_url": f"http://8000/{generated_short_url}"},
        }
    except Exception:
        response.status_code = 500
        return {
            "status": "error",
            "message": "Something went wrong.",
        }
