import os
from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.documents import Document
from pypdf import PdfReader
import io

mcp=FastMCP(name="Google Drive MCP")
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
    try:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        service = build("drive", "v3", credentials=creds)

        return service
    except Exception as e:
        print(e)


def read_pdf_from_drive(service, file_id, file_name):

    request = service.files().get_media(
        fileId=file_id
    ).execute()

    # Memory only — nothing is saved to disk
    pdf_buffer = io.BytesIO(request)


    reader = PdfReader(pdf_buffer)

    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={
                "source": file_name,
                "file_id": file_id,
                "page": i + 1,
            }
        )
        for i, page in enumerate(reader.pages)
        if page.extract_text()
    ]

@mcp.tool()
def google_drive_mcp_server():
    try:
        service=get_drive_service()

        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)",q="trashed = false and mimeType = 'application/pdf'")
            .execute()
        )
        files = results.get("files", [])
        documents = []

        if not files:
            return []

        for file in files:
            documents.extend(read_pdf_from_drive(service, file["id"], file["name"]))

        return documents
    except Exception as e:
        print(e)



if __name__ == '__main__':
    mcp.run(transport="http",port=8081)