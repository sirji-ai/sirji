export class AgentStackManager {
    private agentCallStack: string;
  
    constructor(initialStack: string = "") {
        this.agentCallStack = initialStack;
    }
  
    // Function to add an agent ID to the call stack
    public addAgentId(agentId: string): void {
        if (this.agentCallStack.length > 0) {
            this.agentCallStack += `.${agentId}`;
        } else {
            this.agentCallStack = agentId;
        }
    }
  
    // Function to remove the last agent ID from the call stack
    public removeLastAgentId(): void {
        const ids = this.agentCallStack.split('.');
        ids.pop(); // Remove the last element
        this.agentCallStack = ids.join('.');
    }
  
    // Utility method to view the current stack
    public getStack(): string {
        return this.agentCallStack;
    }
  }