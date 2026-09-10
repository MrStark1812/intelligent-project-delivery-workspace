const API_URL = "http://127.0.0.1:8000";

export const getProjects = async () => {
  const response = await fetch(`${API_URL}/projects`);

  if (!response.ok) {
    throw new Error("Failed to load projects");
  }

  return response.json();
};

export const importProjectFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/import/file`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to import project file"
    );
  }

  return data;
};

export const createProject = async (project) => {
  const response = await fetch(`${API_URL}/projects`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(project),
  });

  if (!response.ok) {
    throw new Error("Failed to create project");
  }

  return response.json();
};

export const getTasks = async (projectId) => {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks`
  );

  if (!response.ok) {
    throw new Error("Failed to load tasks");
  }

  return response.json();
};

export const createTask = async (projectId, task) => {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(task),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to create task");
  }

  return response.json();
};

export const updateTask = async (projectId, taskId, task) => {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks/${taskId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(task),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to update task");
  }

  return response.json();
};

export const getProjectIntelligence = async (projectId) => {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/intelligence`
  );

  if (!response.ok) {
    throw new Error("Failed to load project intelligence");
  }

  return response.json();
};

export const getProjectAIEvaluation = async (projectId) => {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/ai-evaluation`
  );

  if (!response.ok) {
    throw new Error("Failed to load AI project evaluation");
  }

  return response.json();
};