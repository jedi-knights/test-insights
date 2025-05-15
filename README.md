# Test Insights

**Test Insights** is a lightweight Go + HTMX web application for analyzing test suite runs. It helps QA engineers and developers uncover patterns like flaky tests, performance bottlenecks, and failure trends in automated test pipelines.

---

## 🚀 Features

- 📈 Visualize test suite runs
- 🔁 Identify flaky tests based on run history
- 🐢 Track the top N slowest tests
- 📊 View average failures per suite over time
- ⚡ Fast, server-rendered UI using HTMX
- 🧩 Modular Go architecture using `http.ServeMux`

---

## 📂 Project Structure

```
test-insights/
├── cmd/
│   └── server/         # App entrypoint (main.go)
├── internal/
│   ├── handlers/       # HTTP handlers
│   ├── templates/      # HTML templates (Go templates)
│   └── testdata/       # Core domain logic
├── static/             # CSS/JS assets
├── go.mod
└── README.md
```

---

## 🛠 Getting Started

### Prerequisites

- Go 1.22+
- Make (optional) or just the Go CLI

### Installation

```bash
git clone https://github.com/yourusername/test-insights.git
cd test-insights
go mod tidy
go run ./cmd/server
```

Visit `http://localhost:8080` to get started.

---

## 🧠 Technologies Used

- [Go](https://golang.org/)
- [HTMX](https://htmx.org/)
- [Go Templates](https://pkg.go.dev/html/template)

---


## 🛠 Development Tasks (Taskfile)

Use [Task](https://taskfile.dev/) to manage common development tasks:

| Task Name      | Description                                |
|----------------|--------------------------------------------|
| `task build`   | Compile the Go binary                      |
| `task run`     | Run the application locally                |
| `task lint`    | Lint code using go vet, staticcheck, and golangci-lint |
| `task test`    | Run all Go tests                           |
| `task docker-build` | Build the Docker image                 |
| `task docker-run`   | Run the Docker container               |

To run a task:

```bash
task <task-name>
```

Install Task:
```bash
brew install go-task/tap/go-task  # macOS
```

---

## 📌 Roadmap

- [ ] Add database integration
- [ ] Track test trends over time
- [ ] Export reports as CSV/JSON
- [ ] Tag and comment on flaky tests
- [ ] Role-based access control (RBAC)
- [ ] HTMX filtering and live updates

---

## 🧪 Example Use Cases

- Quickly identify unstable test cases that frequently fail
- Track suite performance degradation over time
- Enable QA visibility into test health metrics

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

---

## 📄 License

MIT License © 2025 [Your Name]  
See [LICENSE](LICENSE) for more information.
