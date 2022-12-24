package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

type Config struct {
	Port      string `json:"port"`
	TLSConfig struct {
		CertFile string `json:"cert_file"`
		KeyFile  string `json:"key_file"`
	} `json:"tls_config"`
	StaticDir   string `json:"static_dir"`
	TemplateDir string `json:"template_dir"`

	RepoConfig struct {
		Version    string `json:"version"`
		Author     string `json:"author"`
		Product    string `json:"product"`
		Repository string `json:"repository"`
	} `json:"repo_config"`
}

func main() {
	router := mux.NewRouter()

	configData, err := ioutil.ReadFile("config.json")
	if err != nil {
		log.Fatal(err)
	}

	var config Config
	if err := json.Unmarshal(configData, &config); err != nil {
		log.Fatal(err)
	}

	fs := http.FileServer(http.Dir(config.StaticDir))
	fmt.Print("Hello, World! The current version of gowebserver is v" + config.RepoConfig.Version + ", created by " + config.RepoConfig.Author)
	fmt.Print(".\n--------------------------------------------------------------------------------------------\n")
	fmt.Print("To exit the program, enter the key combination \"CTRL + C\".\n")
	fmt.Print("Site URL: http://localhost" + config.Port + "\n")
	router.PathPrefix("/").Handler(http.StripPrefix("/", fs))

	http.ListenAndServe(config.Port, router)
}
