FROM ai-web:v2

WORKDIR /home/wouldd/code/

COPY web_ui /home/wouldd/code/web_ui
EXPOSE 5000/tcp
EXPOSE 80/tcp
ENV FLASK_APP=web_ui
CMD flask run -h 0.0.0.0 --cert=/etc/letsencrypt/live/ai.makergeek.co.uk/fullchain.pem --key=/etc/letsencrypt/live/ai.makergeek.co.uk/privkey.pem
