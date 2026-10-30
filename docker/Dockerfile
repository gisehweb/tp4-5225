# TP4 - Imagen de GoAccess sobre Alpine Linux - Gisella Henriquez (Legajo 5225)
FROM alpine:3.20

# Instalar GoAccess (sin guardar la caché de apk para que la imagen sea liviana)
RUN apk add --no-cache goaccess

# Usuario no-root por seguridad y carpetas de trabajo con su propietario
RUN addgroup -S analista \
 && adduser -S -D -H -G analista analista \
 && mkdir -p /srv/logs /srv/report /etc/goaccess \
 && chown analista:analista /srv/logs /srv/report

USER analista
WORKDIR /srv

# Puerto del WebSocket para el reporte en tiempo real
EXPOSE 7890

# Espera a que Nginx cree /srv/logs/access.log y luego inicia GoAccess
# con la configuración de /etc/goaccess/goaccess.conf
CMD ["/bin/sh", "-c", "until [ -f /srv/logs/access.log ]; do echo 'Esperando /srv/logs/access.log...'; sleep 2; done; exec goaccess -p /etc/goaccess/goaccess.conf"]
