FROM jac18281828/pythondev:latest

WORKDIR /workspaces/fetch_adblocker

COPY --chown=jac:jac . .

ENV USER=jac
USER jac
