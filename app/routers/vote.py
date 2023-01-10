from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id: {current_user.id} has already voted on post with id: {vote.post_id}")
        db.add(models.Vote(post_id=vote.post_id, user_id=current_user.id))
        db.commit()
        return {"message": "successfully added vote"}

    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="vote direction is either 0 or 1")
