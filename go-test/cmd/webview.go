package main

import (
	"fmt"
	"github.com/jessevdk/go-flags"
	"github.com/polevpn/webview"
	"os"
)

type Option struct {
	Url string `short:"u" long:"url" required:"false" default:"https://fanyi.baidu.com/#en/zh/ABC" description:"URL to be accessed"`
}

func main() {
	var options Option
	if _, err := flags.ParseArgs(&options, os.Args); err != nil {
		fmt.Printf("%s\n", err)
		os.Exit(1)
	}

	w := webview.New(800, 600, false, true)
	defer w.Destroy()
	w.SetTitle("Minimal webview example")
	w.SetSize(800, 600, webview.HintNone)

	//fmt.Println(options.Url)
	w.Navigate(options.Url)
	w.Run()
}
