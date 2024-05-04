package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"testing"
	"time"
)

func TestCristianAlgorithm(t *testing.T) {
	// Define list of time differences
	timeDifferences := []time.Duration{
		-50 * time.Millisecond,
		0 * time.Millisecond,
		50 * time.Millisecond,
	}

	// Define expected range of synchronized time
	expectedMin := -100 * time.Millisecond
	expectedMax := 100 * time.Millisecond

	// Start server in a goroutine
	go func() {
		main()
	}()

	for _, timeDiff := range timeDifferences {

		// Allow some time for the server to start
		time.Sleep(100 * time.Millisecond)

		// Connect to the server
		conn, err := net.Dial("tcp", "localhost:4956")
		if err != nil {
			t.Fatalf("Failed to connect to server: %v", err)
		}

		// Generate mock request with time difference
		requestTime := time.Now().Add(timeDiff)
		fmt.Fprintf(conn, "%s\n", requestTime.Format(time.RFC3339Nano))

		// Receive and parse server response
		response, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			t.Fatalf("Failed to read response: %v", err)
		}
		response = strings.TrimSpace(response)
		receivedTime, err := time.Parse(time.RFC3339Nano, response)
		if err != nil {
			t.Fatalf("Failed to parse response time: %v", err)
		}

		// Calculate the round-trip time
		roundTripTime := time.Since(requestTime)

		// Calculate the clock offset
		clockOffset := receivedTime.Sub(requestTime.Add(roundTripTime / 2))

		// Output metrics
		t.Logf("Request Time:    %s", requestTime.Format(time.RFC3339Nano))
		t.Logf("Received Time:   %s", receivedTime.Format(time.RFC3339Nano))
		t.Logf("Round-Trip Time: %s", roundTripTime)
		t.Logf("Clock Offset:    %s", clockOffset)

		// Check if received time falls within expected range
		if clockOffset < expectedMin || clockOffset > expectedMax {
			t.Errorf("Clock offset %s not within expected range [%s, %s]", clockOffset, expectedMin, expectedMax)
		}
		conn.Close()
	}
}
