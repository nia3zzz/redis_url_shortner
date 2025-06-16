from fastapi import APIRouter, Request, Response
from validators.shortner_validators import (
    CreateShortURLValidator,
    RedirectedShortURLValidator,
)
from pydantic import ValidationError
import string
import random
from utils.redis_client import redis_client
from fastapi.responses import RedirectResponse

router = APIRouter()


# api route function for the creation of the short url from a long url
@router.post("/shortner/")
async def create_short_url(request: Request, response: Response):
    # access the request body of data in the request
    req_body = await request.json()

    try:
        # validate the request body
        validated_req_body = CreateShortURLValidator(url=req_body.get("url").strip())

    except ValidationError as e:

        response.status_code = 401
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


# api route function for getting the already created short url by providing the long url
@router.get("/shortner/")
async def get_short_url(request: Request, response: Response):
    # access the request body of the sent request from the client
    req_body = await request.json()

    try:
        # validate the request body using the create short url validator as it has the same value in both the route functions
        validated_req_body = CreateShortURLValidator(url=req_body.get("url").strip())

    except ValidationError as e:

        response.status_code = 401
        return {
            "status": "error",
            "message": "Failed in type validation.",
            "errors": e.errors(),
        }

    try:
        # retrieve the shortened url in the redis database if not exists send back error message
        check_shortened_url_exists = redis_client.get(validated_req_body.url)

        if check_shortened_url_exists == None:
            response.status_code = 404
            return {"status": "error", "message": "Shortened URL was not found."}

        response.status_code = 200
        return {
            "status": "success",
            "message": "Shortened URL was found.",
            "data": {"shortened_url": f"http://8000/{check_shortened_url_exists}"},
        }
    except Exception:
        response.status_code = 500
        return {"status": "error", "message": "Something went wrong."}


# api route controller function for implimenting deletion of a url key in the memory database
@router.delete("/shortner/")
async def delete_short_url(request: Request, response: Response):
    # get hold of the url that is inside the request object
    req_body = await request.json()

    try:
        # validate the request body send error message to client
        validated_req_body = CreateShortURLValidator(url=req_body.get("url").strip())
    except ValidationError as e:
        response.status_code = 400
        return {
            "status": "error",
            "message": "Failed in type validation.",
            "errors": e.errors(),
        }

    try:
        # check if the key using the provided url exists in redis database
        check_url_key_exists = redis_client.get(validated_req_body.url)

        if check_url_key_exists == None:
            response.status_code = 404
            return {"status": "error", "message": "Shortened URL doesn't exist."}

        # delete the key from the redis database
        check_url_key_exists = redis_client.delete(validated_req_body.url)

        response.status_code = 200
        return {"status": "success", "message": "Shortened URL has been deleted."}

    except Exception:
        response.status_code = 500
        return {"status": "error", "message": "Something went wrong."}


# api route controller function used for redirecting the user to their requested shortened url
@router.post("/shortner/{shortened_url}")
async def redirected_short_url(shortened_url, response: Response):
    try:
        # validate the request url path parameter of shortened url
        validated_req_url_parameter = RedirectedShortURLValidator(
            shortened_url=shortened_url
        )

    except ValidationError as e:
        response.status_code = 400
        return {
            "status": "error",
            "message": "Failed in type validation.",
            "errors": e.errors(),
        }

    try:
        # check if there exists any key in the redis database using the path provided key
        for key in redis_client.scan_iter("*"):
            value = redis_client.get(key)
        if value == validated_req_url_parameter.shortened_url:
            return RedirectResponse(url=key, status_code=302)

        response.status_code = 404
        return {
            "status": "error",
            "message": "This shortened URL is invalid or is not found.",
        }

    except Exception:
        response.status_code = 500
        return {"status": "error", "message": "Something went wrong."}
