from fastapi import status


def get_status_code(err):
    match str(err):
        case (
            "Not found"
            | "Product not found"
            | "Order not found"
            | "User not found"
            | "Users not found"
        ):
            return status.HTTP_404_NOT_FOUND
        case "Not authorized":
            return status.HTTP_401_UNAUTHORIZED
        case "Permission denied":
            return status.HTTP_403_FORBIDDEN
        case _:
            return status.HTTP_400_BAD_REQUEST
