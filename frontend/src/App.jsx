import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const fetchProjects = async () => {
    try {
      setError("");

      const response = await fetch(`${API_URL}/projects`);

      if (!response.ok) {
        throw new Error("Failed to load projects");
      }

      const data = await response.json();
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const createProject = async (event) => {
    event.preventDefault();

    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }

    try {
      setCreating(true);
      setError("");

      const response = await fetch(`${API_URL}/projects`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          description: description || null,
          status: "Not Started",
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create project");
      }

      const newProject = await response.json();

      setProjects((currentProjects) => [
        ...currentProjects,
        newProject,
      ]);

      setName("");
      setDescription("");
    } catch (err) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Intelligent Project Delivery Workspace</h1>
          <p>
            Manage projects, identify risks, and generate actionable
            delivery insights.
          </p>
        </div>
      </header>

      <main className="workspace">
        <section className="card">
          <h2>Create Project</h2>

          <form onSubmit={createProject}>
            <label htmlFor="project-name">Project Name</label>

            <input
              id="project-name"
              type="text"
              placeholder="Enter project name"
              value={name}
              onChange={(event) => setName(event.target.value)}
            />

            <label htmlFor="project-description">
              Description
            </label>

            <textarea
              id="project-description"
              placeholder="Describe the project"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              rows="4"
            />

            <button type="submit" disabled={creating}>
              {creating ? "Creating..." : "Create Project"}
            </button>
          </form>
        </section>

        <section className="card">
          <div className="section-header">
            <h2>Projects</h2>

            <button
              className="secondary-button"
              onClick={fetchProjects}
              disabled={loading}
            >
              Refresh
            </button>
          </div>

          {error && <p className="error">{error}</p>}

          {loading ? (
            <p>Loading projects...</p>
          ) : projects.length === 0 ? (
            <p className="empty-state">
              No projects yet. Create your first project above.
            </p>
          ) : (
            <div className="project-list">
              {projects.map((project) => (
                <article className="project" key={project.id}>
                  <div>
                    <h3>{project.name}</h3>

                    <p>
                      {project.description ||
                        "No description provided."}
                    </p>
                  </div>

                  <span className="status">
                    {project.status}
                  </span>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;