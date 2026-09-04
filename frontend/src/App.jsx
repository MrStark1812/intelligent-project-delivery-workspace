import { useEffect, useState } from "react";
import "./App.css";

import {
  createProject as createProjectApi,
  createTask as createTaskApi,
  getProjects,
  getTasks,
  getProjectIntelligence,
  updateTask,
} from "./services/api";

function App() {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [tasksLoading, setTasksLoading] = useState(false);
  const [tasksError, setTasksError] = useState("");
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editStatus, setEditStatus] = useState("");
  const [editPriority, setEditPriority] = useState("");
  const [savingTask, setSavingTask] = useState(false);
  const [taskCreating, setTaskCreating] = useState(false);

  const [taskName, setTaskName] = useState("");
  const [taskDescription, setTaskDescription] = useState("");
  const [taskPriority, setTaskPriority] = useState("Medium");
  const [taskDueDate, setTaskDueDate] = useState("");
  const [taskEstimatedHours, setTaskEstimatedHours] = useState("");

  const [intelligence, setIntelligence] = useState(null);
  const [intelligenceLoading, setIntelligenceLoading] = useState(false);
  const [intelligenceError, setIntelligenceError] = useState("");

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const fetchProjects = async () => {
  try {
    setError("");

    const data = await getProjects();
    setProjects(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  const fetchTasks = async (projectId) => {
  try {
    setTasksLoading(true);
    setTasksError("");

    const data = await getTasks(projectId);
    setTasks(data);
  } catch (err) {
    setTasksError(err.message);
    setTasks([]);
  } finally {
    setTasksLoading(false);
  }
};

  const fetchIntelligence = async (projectId) => {
  try {
    setIntelligenceLoading(true);
    setIntelligenceError("");

    const data = await getProjectIntelligence(projectId);
    setIntelligence(data);
  } catch (err) {
    setIntelligenceError(err.message);
    setIntelligence(null);
  } finally {
    setIntelligenceLoading(false);
  }
};

const startEditingTask = (task) => {
  setEditingTaskId(task.id);
  setEditStatus(task.status);
  setEditPriority(task.priority);
};

const cancelEditingTask = () => {
  setEditingTaskId(null);
  setEditStatus("");
  setEditPriority("");
};

const saveTask = async (taskId) => {
  try {
    setSavingTask(true);
    setTasksError("");

    const updatedTask = await updateTask(
      selectedProjectId,
      taskId,
      {
        status: editStatus,
        priority: editPriority,
      }
    );

    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === taskId ? updatedTask : task
      )
    );

    cancelEditingTask();
  } catch (err) {
    setTasksError(err.message);
  } finally {
    setSavingTask(false);
  }
};

  const totalTasks = intelligence?.total_tasks ?? 0;
const completedTasks = intelligence?.completed_tasks ?? 0;
const inProgressTasks = intelligence?.in_progress_tasks ?? 0;
const notStartedTasks = intelligence?.not_started_tasks ?? 0;
const completionPercentage =
  intelligence?.completion_percentage ?? 0;

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
  if (!selectedProjectId) {
    setTasks([]);
    setIntelligence(null);
    return;
  }

  fetchTasks(selectedProjectId);
  fetchIntelligence(selectedProjectId);
}, [selectedProjectId]);

  const createProject = async (event) => {
    event.preventDefault();

    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }

    try {
  setCreating(true);
  setError("");

  const newProject = await createProjectApi({
    name,
    description: description || null,
    status: "Not Started",
  });

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

    const createTask = async (event) => {
    event.preventDefault();

    if (!selectedProjectId) {
      setTasksError("Please select a project first.");
      return;
    }

    if (!taskName.trim()) {
      setTasksError("Task name is required.");
      return;
    }

    try {
      setTaskCreating(true);
      setTasksError("");

      const newTask = await createTaskApi(selectedProjectId, {
        name: taskName,
        description: taskDescription || null,
        status: "Not Started",
        priority: taskPriority,
        due_date: taskDueDate || null,
        estimated_hours: taskEstimatedHours
          ? Number(taskEstimatedHours)
          : null,
        actual_hours: null,
      });

      setTasks((currentTasks) => [
        ...currentTasks,
        newTask,
      ]);

      setTaskName("");
      setTaskDescription("");
      setTaskPriority("Medium");
      setTaskDueDate("");
      setTaskEstimatedHours("");
    } catch (err) {
      setTasksError(err.message);
    } finally {
      setTaskCreating(false);
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
                <article
                  className={`project ${
                    selectedProjectId === project.id ? "selected" : ""
                  }`}
                  key={project.id}
                  onClick={() => setSelectedProjectId(project.id)}
               >
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

                <section className="card">
                  <div className="section-header">
                    <h2>Project Dashboard</h2>
                  </div>

                  {!selectedProjectId ? (
                    <p className="empty-state">
                      Select a project to view delivery metrics.
                    </p>
                  ) : (
                    <>
                      <div className="metrics">
                        <div className="metric">
                          <span className="metric-label">Total Tasks</span>
                          <strong>{totalTasks}</strong>
                        </div>

                        <div className="metric">
                          <span className="metric-label">Completed</span>
                          <strong>{completedTasks}</strong>
                        </div>

                        <div className="metric">
                          <span className="metric-label">In Progress</span>
                          <strong>{inProgressTasks}</strong>
                        </div>

                        <div className="metric">
                          <span className="metric-label">Not Started</span>
                          <strong>{notStartedTasks}</strong>
                        </div>

                        <div className="metric">
                          <span className="metric-label">Completion</span>
                          <strong>{completionPercentage}%</strong>
                        </div>
                                            </div>

                                            <div className="progress-section">
                        <div className="progress-header">
                          <span>Project Completion</span>
                          <strong>{completionPercentage}%</strong>
                        </div>

                        <div className="progress-bar">
                          <div
                            className="progress-fill"
                            style={{ width: `${completionPercentage}%` }}
                          />
                        </div>
                      </div>

                      <div className="intelligence-section">
                        <div className="metrics">
                          <div className="metric">
                            <span className="metric-label">Overdue Tasks</span>
                            <strong>
                              {intelligence?.overdue_tasks ?? 0}
                            </strong>
                          </div>

                          <div className="metric">
                            <span className="metric-label">Estimated Hours</span>
                            <strong>
                              {intelligence?.estimated_hours ?? 0}
                            </strong>
                          </div>

                          <div className="metric">
                            <span className="metric-label">Actual Hours</span>
                            <strong>
                              {intelligence?.actual_hours ?? 0}
                            </strong>
                          </div>

                          <div className="metric">
                            <span className="metric-label">Effort Variance</span>
                            <strong>
                              {intelligence?.effort_variance ?? 0}
                            </strong>
                          </div>

                          <div className="metric">
                            <span className="metric-label">Variance %</span>
                            <strong>
                              {intelligence?.effort_variance_percentage ?? 0}%
                            </strong>
                          </div>
                        </div>

                        <div className="risk-summary">
                          <div>
                            <span className="metric-label">Schedule Risk</span>
                            <strong
                              className={`risk-value risk-${(
                                intelligence?.schedule_risk || ""
                              ).toLowerCase()}`}
                            >
                            {intelligence?.schedule_risk ?? "—"}
                          </strong>
                        </div>

                          <div>
                            <span className="metric-label">Effort Risk</span>
                            <strong
                              className={`risk-value risk-${(
                                intelligence?.effort_risk || ""
                              ).toLowerCase()}`}
                            >
                              {intelligence?.effort_risk ?? "—"}
                            </strong>
                          </div>

                          <div>
                            <span className="metric-label">Project Health</span>
                            <strong
                              className={`risk-value health-${(
                                intelligence?.project_health || ""
                              )
                                .toLowerCase()
                                .replace(/\s+/g, "-")}`}
                            >
                              {intelligence?.project_health ?? "—"}
                            </strong>
                          </div>
                        </div>
                                            </div>

                      <div className="ai-insights">
                        <div className="section-header">
                          <h3>AI Delivery Insights</h3>
                        </div>

                        {intelligenceLoading ? (
                          <p>Generating project insights...</p>
                        ) : intelligenceError ? (
                          <p className="error">{intelligenceError}</p>
                        ) : intelligence?.ai_evaluation ? (
                          <>
                            <div className="ai-health">
                              <span className="metric-label">
                                Health Assessment
                              </span>

                              <p>
                                {intelligence.ai_evaluation.health_assessment}
                              </p>
                            </div>

                            <div className="ai-columns">
                              <div>
                                <span className="metric-label">
                                  Risks
                                </span>

                                {intelligence.ai_evaluation.risks.length === 0 ? (
                                  <p className="empty-state">
                                    No current risks identified.
                                  </p>
                                ) : (
                                  <ul>
                                    {intelligence.ai_evaluation.risks.map(
                                      (risk, index) => (
                                        <li key={index}>{risk}</li>
                                      )
                                    )}
                                  </ul>
                                )}
                              </div>

                              <div>
                                <span className="metric-label">
                                  Schedule Concerns
                                </span>

                                {intelligence.ai_evaluation.schedule_concerns.length === 0 ? (
                                  <p className="empty-state">
                                    No schedule concerns identified.
                                  </p>
                                ) : (
                                  <ul>
                                    {intelligence.ai_evaluation.schedule_concerns.map(
                                      (concern, index) => (
                                        <li key={index}>{concern}</li>
                                      )
                                    )}
                                  </ul>
                                )}
                              </div>

                              <div>
                                <span className="metric-label">
                                  Effort Concerns
                                </span>

                                {intelligence.ai_evaluation.effort_concerns.length === 0 ? (
                                  <p className="empty-state">
                                    No effort concerns identified.
                                  </p>
                                ) : (
                                  <ul>
                                    {intelligence.ai_evaluation.effort_concerns.map(
                                      (concern, index) => (
                                        <li key={index}>{concern}</li>
                                      )
                                    )}
                                  </ul>
                                )}
                              </div>

                              <div>
                                <span className="metric-label">
                                  Problem Areas
                                </span>

                                {intelligence.ai_evaluation.problem_areas.length === 0 ? (
                                  <p className="empty-state">
                                    No problem areas identified.
                                  </p>
                                ) : (
                                  <ul>
                                    {intelligence.ai_evaluation.problem_areas.map(
                                      (problem, index) => (
                                        <li key={index}>{problem}</li>
                                      )
                                    )}
                                  </ul>
                                )}
                              </div>
                            </div>
                          </>
                        ) : (
                          <p className="empty-state">
                            AI insights are not available.
                          </p>
                        )}
                      </div>
                    </>
                  )}
                </section>

        <section className="card">
          <div className="section-header">
            <h2>Tasks</h2>
          </div>
                    {selectedProjectId && (
            <form onSubmit={createTask}>
              <label htmlFor="task-name">Task Name</label>

              <input
                id="task-name"
                type="text"
                placeholder="Enter task name"
                value={taskName}
                onChange={(event) =>
                  setTaskName(event.target.value)
                }
              />

              <label htmlFor="task-description">
                Description
              </label>

              <textarea
                id="task-description"
                placeholder="Describe the task"
                value={taskDescription}
                onChange={(event) =>
                  setTaskDescription(event.target.value)
                }
                rows="3"
              />

              <label htmlFor="task-priority">Priority</label>

              <select
                id="task-priority"
                value={taskPriority}
                onChange={(event) =>
                  setTaskPriority(event.target.value)
                }
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>

              <label htmlFor="task-due-date">Due Date</label>

              <input
                id="task-due-date"
                type="date"
                value={taskDueDate}
                onChange={(event) =>
                  setTaskDueDate(event.target.value)
                }
              />

              <label htmlFor="task-estimated-hours">
                Estimated Hours
              </label>

              <input
                id="task-estimated-hours"
                type="number"
                min="0"
                step="0.5"
                placeholder="e.g. 4"
                value={taskEstimatedHours}
                onChange={(event) =>
                  setTaskEstimatedHours(event.target.value)
                }
              />

              <button type="submit" disabled={taskCreating}>
                {taskCreating ? "Creating..." : "Create Task"}
              </button>
            </form>
          )}

          {!selectedProjectId ? (
            <p className="empty-state">
              Select a project to view its tasks.
            </p>
          ) : tasksLoading ? (
            <p>Loading tasks...</p>
          ) : tasksError ? (
            <p className="error">{tasksError}</p>
          ) : tasks.length === 0 ? (
            <p className="empty-state">
              No tasks for this project yet.
            </p>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <article className="task" key={task.id}>
            <div>
              <h3>{task.name}</h3>

              <p>
                {task.description ||
                  "No description provided."}
              </p>
            </div>

            {editingTaskId === task.id ? (
              <div className="task-edit">
                <select
                  value={editStatus}
                  onChange={(event) =>
                    setEditStatus(event.target.value)
                  }
                >
                  <option value="Not Started">Not Started</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>

                <select
                  value={editPriority}
                  onChange={(event) =>
                    setEditPriority(event.target.value)
                  }
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>

                <button
                  onClick={() => saveTask(task.id)}
                  disabled={savingTask}
                >
                  {savingTask ? "Saving..." : "Save"}
                </button>

                <button
                  className="secondary-button"
                  onClick={cancelEditingTask}
                  disabled={savingTask}
                >
                  Cancel
                </button>
              </div>
            ) : (
              <div className="task-meta">
                <span className="status">
                  {task.status}
                </span>

                <span className="priority">
                  {task.priority}
                </span>

                <button
                  onClick={() => startEditingTask(task)}
                >
                  Edit
                </button>
              </div>
            )}
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
