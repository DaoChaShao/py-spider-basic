'''
200 OK                    // 客户端请求成功
301 Moved Permanently     // 资源被永久移动到新地址
400 Bad Request           // 客户端不能被服务器所理解
401 Unauthorized          // 请求未经授权
403 Forbidden             // 服务器拒绝提供服务
404 Not Found             // 请求资源不存在
500 Internal Server       // 服务器发生不可预期的错误
503 Service Unavailable   // 服务器当前不能处理客户端的请求
'''

from random import choice


def response_status(code: int):
    if code == 200:
        print(f'请求反馈：OK，客户端请求成功')
    elif code == 301:
        print(f'请求反馈：Moved Permanently，资源被永久移动到新地址')
    elif code == 400:
        print(f'请求反馈：Bad Request，客户端不能被服务器所理解')
    elif code == 401:
        print(f'请求反馈：Unauthorized，请求未经授权')
    elif code == 403:
        print(f'请求反馈：Forbidden，服务器拒绝提供服务')
    elif code == 404:
        print(f'请求反馈：Not Found，请求资源不存在')
    elif code == 500:
        print(f'请求反馈：Internal Server，服务器发生不可预期的错误')
    elif code == 503:
        print(f'请求反馈：Service Unavailable，服务器当前不能处理客户端的请求')
    else:
        print('其他未知问题！')


def response_feedback(code: int) -> str:
    status_code = {
        200: "OK / 客户端请求成功",
        301: "Moved Permanently / 资源被永久移动到新地址",
        400: "Bad Request / 客户端不能被服务器所理解",
        401: "Unauthorized / 请求未经授权",
        403: "Forbidden / 服务器拒绝提供服务",
        404: "Not Found / 请求资源不存在",
        500: "Internal Server / 服务器发生不可预期的错误",
        503: "Service Unavailable / 服务器当前不能处理客户端的请求",
    }
    result = status_code.get(code, "其他未知问题")
    return result


def main():
    print(response_feedback(choice([200, 301, 400, 401, 403, 404, 500, 503])))
    print(response_feedback(choice([200, 301, 400, 401, 403, 404, 500, 503])))


if __name__ == "__main__":
    main()
