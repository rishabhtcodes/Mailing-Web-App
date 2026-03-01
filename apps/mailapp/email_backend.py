from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
import smtplib


class PatchedEmailBackend(SMTPBackend):
    def open(self):
        if self.connection:
            return False

        connection_params = {}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout

        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )

            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except (smtplib.SMTPException, OSError):
            if not self.fail_silently:
                raise
