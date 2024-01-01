FROM golang:1.21.5 as builder
WORKDIR /app
COPY main.go .
COPY go.mod .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o multiport-listener .

FROM scratch
COPY --from=builder /app/multiport-listener .
