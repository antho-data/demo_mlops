from fastapi import Depends, APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import FileResponse
from app.library.security import check_authenticated, check_is_admin
from app.library.logging import log_usage
from app.yolo_interface.predictor import Predictor
from app.database.database_init import get_log_session
from sqlalchemy.orm import Session
from app.data_mappers.data_mappers import User

# API instanciation

router = APIRouter(
    tags=["Object detection"],
	responses = {401: {"description": "Not authenticated"}},
)

responses = {
    408: {"description": "Image invalid"}
}

@router.post("/detection", description="Perform object detection", responses=responses)
async def detection(request : Request, 
					file: UploadFile,
					db: Session = Depends(get_log_session), 
					user: User = Depends(check_authenticated)):
	log_usage(db, user.id, request)        
	try:
		#  Save input image by chunks of 1 MB
		with open("input/"+file.filename, 'wb') as f:
			while contents := file.file.read(1024*1024):
				f.write(contents)
		success = True
	except Exception:
		success = False
	finally:
		file.file.close()

	pred = Predictor()
	result_file = pred.predict(file.filename)
	pred.clean_up_folders(True, False)
	return FileResponse(result_file)


