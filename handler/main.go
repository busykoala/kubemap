package main

import (
    "fmt"
    "net"
    "os"
    "os/signal"
    "strings"
    "sync"
    "syscall"
    "time"
)

func handleConnections(port int) {
    listener, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%d", port))
    if err != nil {
        fmt.Printf("Error listening on port %d: %v\n", port, err)
        return
    }
    defer listener.Close()

    for {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }

        fmt.Printf("%s connected on port %d\n", conn.RemoteAddr().String(), port)
        conn.Close()
    }
}

func startListener() {
    ports := []int{8042} // Define your ports here

    for _, port := range ports {
        go handleConnections(port)
    }

    sigs := make(chan os.Signal, 1)
    signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

    <-sigs
    fmt.Println("\nShutting down...")
}

func checkPort(wg *sync.WaitGroup, ip string, port int) {
    defer wg.Done()
    
    address := fmt.Sprintf("%s:%d", ip, port)
    conn, err := net.DialTimeout("tcp", address, 5*time.Second)
    if err != nil {
        fmt.Printf("Connection to %s failed: %v\n", address, err)
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
    fmt.Println("\nAll checks complete. Shutting down...")
}

func main() {
    if len(os.Args) > 1 {
        ips := strings.Split(os.Args[1], ";")
        startChecker(ips)
    } else {
        startListener()
    }
}
