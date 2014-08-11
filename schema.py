from sqlalchemy import Column, DateTime, String, Integer, Text, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Web(Base):
  __tablename__ = "webs"
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), nullable=False)
  name = Column(String(60), default="", nullable=False)
  address = Column(String(60), default="", nullable=False)
  password = Column(String(60))
  additional_style = Column(Text(255))
  allow_uploads = Column(Integer, default=1)
  published = Column(Integer, default=0)
  count_pages = Column(Integer, default=0)
  markup = Column(String(50), default="markdownMML")
  color = Column(String(6), default="008B26")
  max_upload_size = Column(Integer, default=100)
  safe_mode = Column(Integer, default=0)
  brackets_only = Column(Integer, default=0)

class Page(Base):
  __tablename__ = "pages"
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), nullable=False)
  name = Column(String)
  locked_by = Column(String(60))
  locked_at = Column(DateTime)
  web_id = Column(Integer, ForeignKey("webs.id"), default=0, nullable=False)
  web = relationship(Web,
    backref=backref("pages",
      uselist=True,
      cascade="delete,all"))

class Revision(Base):
  __tablename__ = "revisions"
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), nullable=False)
  revised_at = Column(DateTime, default=func.now(), nullable=False)
  content = Column(Text(16777215), default="", nullable=False)
  author = Column(String(60))
  ip = Column(String(60))
  page_id = Column(Integer, ForeignKey("pages.id"), default=0, nullable=False)
  page = relationship(Page,
    backref=backref("revisions",
                     uselist=True,
                     cascade='delete,all'))

class WikiSession(Base):
  __tablename__ = "sessions"
  id = Column("session_id", Integer, primary_key=True)
  data = Column(Text)
  updated_at = Column(DateTime)

class System(Base):
  __tablename__ = "system"
  id = Column(Integer, primary_key=True)
  password = Column(String(60))

class WikiFile(Base):
  __tablename__ = "wiki_files"
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), nullable=False)
  file_name = Column(String, nullable=False)
  description = Column(String, nullable=False)
  web_id = Column(Integer, ForeignKey("webs.id"), default=0, nullable=False)
  web = relationship(Web,
    backref=backref("wiki_files",
      uselist=True,
      cascade="delete,all"))

class WikiReference(Base):
  __tablename__ = "wiki_references"
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), nullable=False)
  referenced = Column(String, default="", nullable=False)
  link_type = Column(String(1), nullable=False)
  page_id = Column(Integer, ForeignKey("pages.id"), default=0, nullable=False)
  page = relationship(Page,
    backref=backref("wiki_references",
      uselist=True,
      cascade="delete,all"))
