FROM golang AS build-env

ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /go/src/github.com/jdamata/k8vault
ADD . /go/src/github.com/jdamata/k8vault
RUN go build -a -tags netgo -ldflags '-w' -o /bin/k8vault

FROM alpine
COPY --from=build-env /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=build-env /bin/k8vault /k8vault
ENTRYPOINT ["/k8vault"]