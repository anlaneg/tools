package main

import "github.com/polevpn/webview"

func main() {

	w := webview.New(800, 600, false, true)
	defer w.Destroy()
	w.SetTitle("Minimal webview example")
	w.SetSize(800, 600, webview.HintNone)
	w.Navigate("https://www.baidu.com")
	w.Run()
}
