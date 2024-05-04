package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"testing"
	"time"
)

func main() {

	message("Launching client")
	conn, err := net.Dial("tcp", "127.0.0.1:4956")
	exitOnError(err)

	before := time.Now()
	message("")
	message("Before:  ", before)
	fmt.Fprintf(conn, before.Format(time.RFC3339Nano)+"\n")

	str, err := bufio.NewReader(conn).ReadString('\n')
	exitOnError(err)
	if len(str) < 1 {
		message("ERR: Invalid string!")
		os.Exit(1)
	}

	received, err := time.Parse(time.RFC3339Nano, str[:len(str)-1])
	exitOnError(err)
	message("Received:", received)

	after := time.Now()
	message("After:   ", after)

	correction := after.Sub(before) / 2

	message("")
	message("Correction: +", correction)
	message("Time is", received.Add(correction))
}

func message(a ...interface{}) (n int, err error) {
	return fmt.Print("[C] ", fmt.Sprintln(a...))
}

func exitOnError(err error) {
	if err != nil {
		message("ERR:", err)
		os.Exit(1)
	}
}

// MockListener mocks net.Listener for testing purposes
type MockDialer struct {
	Conn net.Conn
}

func (md *MockDialer) Dial(network, address string) (net.Conn, error) {
	return md.Conn, nil
}

func TestClient(t *testing.T) {
	// Mock connection for testing client
	mockConn, _ := net.Pipe()
	defer mockConn.Close()

	// Test client
	go main()
	time.Sleep(100 * time.Millisecond) // Allow some time for client execution

	// Receive timestamp from server
	buf := make([]byte, 1024)
	n, _ := mockConn.Read(buf)
	received := string(buf[:n])

	// Parse received timestamp
	parsedTime, err := time.Parse(time.RFC3339Nano, received)
	if err != nil {
		t.Errorf("Failed to parse received timestamp: %v", err)
	}

	// Verify correctness
	if !parsedTime.Before(time.Now()) {
		t.Errorf("Expected timestamp before current time, but received %v", parsedTime)
	}
}
