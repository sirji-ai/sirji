import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';

export interface Session {
  sessionId: string;
  callStack: string;
  timestamp: string;
}

export class SessionManager {
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  public startNewSession(callStack: string): string {
    const newSession: Session = {
      sessionId: uuidv4(),
      callStack: callStack,
      timestamp: new Date().toISOString()
    };
    const data = this.readSessionsFile();
    data.sessions.push(newSession);
    this.writeSessionsFile(data);

    return newSession.sessionId;
  }

  public reuseSession(callStack: string): string | null {
    const data = this.readSessionsFile();
    const filteredSessions: Session[] = data.sessions.filter((session: Session) => session.callStack === callStack);
    if (filteredSessions.length > 0) {
      filteredSessions.sort((a: Session, b: Session) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      return filteredSessions[0].sessionId;
    }

    return null;
  }

  public getCurrentSeesionId(callStack: string): string | null {
    const data = this.readSessionsFile();
    const filteredSessions: Session[] = data.sessions.filter((session: Session) => session.callStack === callStack);
    if (filteredSessions.length > 0) {
      filteredSessions.sort((a: Session, b: Session) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      return filteredSessions[0].sessionId;
    }

    return null;
  }

  public getSessionTimestampMillis(sessionId: string): number | null {
    const data = this.readSessionsFile();
    const session = data.sessions.find((session: Session) => session.sessionId === sessionId);
    if (session) {
      return new Date(session.timestamp).getTime();
    }
    return null;
  }

  private readSessionsFile(): { sessions: Session[] } {
    try {
      const fileContents = fs.readFileSync(this.filePath, 'utf8');
      return JSON.parse(fileContents) as { sessions: Session[] };
    } catch (error) {
      console.error('Error reading the sessions file:', error);
      return { sessions: [] };
    }
  }

  private writeSessionsFile(data: { sessions: Session[] }): void {
    try {
      fs.writeFileSync(this.filePath, JSON.stringify(data, null, 4));
    } catch (error) {
      console.error('Error writing to the sessions file:', error);
    }
  }
}
