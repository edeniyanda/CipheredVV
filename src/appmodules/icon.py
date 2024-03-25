class tellIcon:
    def __init__(self, extention:str) -> None:
        self.extention = extention

    def tell(self):
        extentionIcon:dict = {".pdf" : "pdf.png",
         ".mp3" : "music-notes.png",
         ".txt" : "txt-file.png",
         ".mp4" : "video.png",
         ".docx" : "word.png",
         "xlxs" : "excel.png"}
        
        filename = extentionIcon.get(self.extention)
        return filename