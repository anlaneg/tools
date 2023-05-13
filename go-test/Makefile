all: format-source
	go build cmd/hello.go
	go build cmd/webview.go
	go build cmd/astilectron.go

format-source:
	find . -type f -name '*.go' | xargs -t -I{} go fmt {}

clean:

