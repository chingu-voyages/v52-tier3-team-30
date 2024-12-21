package main

import (
	"database/sql"
	"log"

	"github.com/gin-gonic/gin"
	"github.com/lib/pq"
	"fmt"
)

func main() {
	fmt.Printf("Main function")

	// Get the working directory
	wd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	// Print the working directory
	fmt.Println("Working directory:", wd)

	// Open the SQLite database file
	connStr := "user=hualun dbname=chingu sslmode=verify-full"
	db, err := sql.Open("postgres", connStr)

	defer func(db *sql.DB) {
		err := db.Close()
		if err != nil {
			log.Fatal(err)
		}
	}(db)

	// Create the Gin router
	r := gin.Default()

	if err != nil {
		log.Fatal(err)
	}

	// Creation endpoints
	r.POST("/users", func(c *gin.Context) { createUser(c, db) })

	// Login endpoint
	r.POST("/login", func(c *gin.Context) { login(c, db) })

	err = r.Run(":8080")
	if err != nil {
		log.Fatal(err)
	}
}
