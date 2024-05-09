

class SendEmailContentClient:
    def __init__(self):
        pass
    
    @staticmethod
    def verify_account(url: str) -> str:
        return (f'''
                <!DOCTYPE html>
                <html>
                    <head></head>
                    <body>
                        <h1>Verify your account</h1>
                        <p>Click <a href="{url}">here</a> to verify your account</p>
                    </body>
                </html>
            ''')

    @staticmethod
    def reset_password(url: str) -> str:
        return (f'''
                <!DOCTYPE html>
                <html>
                    <head></head>
                    <body>
                        <h1>Reset your password</h1>
                        <p>Click <a href="{url}">here</a> to reset your password</p>
                    </body>
                </html>
            ''')