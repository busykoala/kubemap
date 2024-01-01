package main

import (
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

func handleConnections(port int, stopChan <-chan struct{}) {
    listener, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%d", port))
    if err != nil {
        return
    }
    defer listener.Close()

    go func() {
        <-stopChan
        listener.Close()
    }()

    for {
        conn, err := listener.Accept()
        if err != nil {
            break
        }

        fmt.Printf("\n")
        conn.Close()
    }
}

func checkPort(wg *sync.WaitGroup, ip string, port int) {
    defer wg.Done()

    address := fmt.Sprintf("%s:%d", ip, port)
    conn, err := net.DialTimeout("tcp", address, 5*time.Second)
    if err != nil {
        return
    }
    defer conn.Close()
    fmt.Printf("Connection to %s succeeded\n", address)
}

func startChecker(ips []string) {
    ports := []int{8042} // Define the ports to check
    var wg sync.WaitGroup

    for _, ip := range ips {
        for _, port := range ports {
            wg.Add(1)
            go checkPort(&wg, ip, port)
        }
    }

    wg.Wait()
}

func main() {
    if len(os.Args) > 1 {
        // Start listener
        stopChan := make(chan struct{})
        doneChan := make(chan struct{}) // Channel to signal completion
        ports := []int{8042} // Ports to listen/check

        for _, port := range ports {
            go handleConnections(port, stopChan)
        }

        // Signal to close the listener
        go func() {
            <-stopChan
            close(doneChan)
        }()

        // Run checker after 20 seconds
        ips := strings.Split(os.Args[1], ";")
        time.AfterFunc(20*time.Second, func() {
            startChecker(ips)
        })

        // Stop listener after 100 seconds
        time.AfterFunc(100*time.Second, func() {
            close(stopChan)
        })

        // Wait for the listener to finish shutting down
        <-doneChan
    } else {
        fmt.Println("No IPs provided. Exiting...")
    }
}
