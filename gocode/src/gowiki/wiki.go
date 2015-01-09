// Package main provides ...
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"html/template"
	"errors"
	"regexp"
	"log"

	_ "net/http/pprof"
)

type Page struct {
	Title	string
	Body	[]byte
}

var templates = template.Must(template.ParseFiles(
	"templates/edit.html", 
	"templates/view.html"))

var validPath = regexp.MustCompile("^/(edit|save|view)/([a-zA-Z0-9]+)$")

func getTitle(w http.ResponseWriter, r *http.Request) (string, error) {
	m := validPath.FindStringSubmatch(r.URL.Path)
	if m == nil {
		http.NotFound(w, r)
		return "", errors.New("Invalid Page Title")
	}
	return m[2], nil
}


func (p *Page) save() error {
	filename := p.Title + ".txt"
	return ioutil.WriteFile(filename, p.Body, 0600)
}


func loadPage(title string) (*Page, error) {
	filename := title + ".txt"
	// check filename existsed?
	body, err := ioutil.ReadFile(filename)
	return &Page{Title: title, Body: body}, err
}


func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
}


func viewHandler(w http.ResponseWriter, r *http.Request) {
	title, err := getTitle(w, r)
	if err != nil {
		return
	}
	p, err := loadPage(title)
	if err != nil {
		http.Redirect(w, r, "/edit/" + title, http.StatusFound)
		return
	}
	renderTemplate(w, "view", p)
}

func saveHandler(w http.ResponseWriter, r *http.Request) {
	title := r.URL.Path[len("/save/"):]
	body := r.FormValue("body")
	p := &Page{Title: title, Body: []byte(body)}
	p.save()
	http.Redirect(w, r, "/view/" + title, http.StatusFound)
}

func editHandler(w http.ResponseWriter, r *http.Request) {
	title, err := getTitle(w, r)
	if err != nil {
		return
	}
	p, err := loadPage(title)
	if err != nil {
		p = &Page{Title: title}
	}
	renderTemplate(w, "edit", p)
}

func renderTemplate(w http.ResponseWriter, tmpl string, p *Page) {
	err := templates.ExecuteTemplate(w, "templates/" + tmpl + ".html", p)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func makeHandler(fn func(http.ResponseWriter, *http.Request, string)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		m := validPath.FindStringSubmatch(r.URL.Path)
		if m == nil {
			http.NotFound(w, r)
			return
		}
		fn(w, r, m[2])
	}
	
}

type User struct {
	Name string
}

func userHandler(w http.ResponseWriter, r *http.Request, user *User) {
	fmt.Fprintf(w, "hello %s", user.Name)
}

func getCurrentUser(r *http.Request) (*User, error) {
	// return nil, errors.New("user not found")
	return &User{"yxy"}, nil
}


func Authenticated(fn func(http.ResponseWriter, *http.Request, *User)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		user, err := getCurrentUser(r)
		if err != nil {
			http.Error(w, err.Error(), 405)
			return
		}
		fn(w, r, user)
	}
}

type Rect struct {
	width int
	height int
}

func (r *Rect) Area() int {
	return r.width * r.height
}

type Foo func() int

func (f Foo) Add(x int) int {
	return f() + x
}

type Address struct {
	Number string
	Street string
	City string
}

type Person struct {
	Name string
	Address
}

func (a *Address) String() string {
	return a.Number + " "
	
}

func (p *Person) String() string {
	return p.Name + " " + p.Address.String()
}

type Counter int

func (ctr *Counter) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	*ctr++
	fmt.Fprintf(w, "counter = %d\n", ctr)
}


func main() {
	// p1 := &Page{Title: "TestPage", Body: []byte("这是一个测试的页面")}
	// p1.save()
	ctr := new(Counter)
	http.Handle("/args/", ctr)
	http.HandleFunc("/view/", viewHandler)
	http.HandleFunc("/save/", saveHandler)
	http.HandleFunc("/edit/", editHandler)
	http.HandleFunc("/user/", Authenticated(userHandler))
	// string == slice of bytes
	var l1 = [...]int{1, 2, 3, 4, 5}
	var l2 = [5] int { 1, 2, 3, 4, 5 }
	names := [] string {"Mary", "Lily"}
	names = append(names, "Jane")
	fmt.Println(l1, l2)
	var x Foo
	x = func() int { return 10 }
	fmt.Println(x.Add(12))
	p := Person{
		Name: "Steve",
		Address: Address{
			Number: "FFF",
			Street: "Street",
			City: "GuangZhou",
		},
	}
	fmt.Println(p.City)
	fmt.Println(p.String())
	fmt.Println(p.Address.String())
	a := new(int)
	log.Println(a)
	fmt.Println(a)
	fmt.Println(*a)

	var b int = 10
	var c *int = &b

	b = 12
	fmt.Println(b, *c)
	// log.Println(http.ListenAndServe("localhost:6060", nil))
}
