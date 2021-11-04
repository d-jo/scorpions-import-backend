
# %%



def from_dict(o, d):
    """
    Update a model from a dictionary
    """
    for k, v in d.items():
        setattr(o, k, v)

class BaseModel:
  """
  Base for all models that contians useful functions
  """
  def init_from_dict(self, d):
    for k, v in d.items():
      setattr(self, k, v)
  
  def to_dict(self):
    d = {}
    for attr in self.__dict__:
      if attr[0] != '_':
        d[attr] = getattr(self, attr)
    return d

class Document(BaseModel):
  __slots__ = [
    'id',
    'title',
    'author',
    'created',
    'college',
    'department',
    'program',
    'degree_level',
    'academic_year',
    'accreditation_body',
    'last_accreditation_review',
    'slos_meet_standards',
    'stakeholder_involvement',
    'additional_information'
  ]
  def __init__(self):
    pass


class SLO(BaseModel):
  def __init__(self):
    pass

class Measure(BaseModel):
  def __init__(self):
    pass

class DecisionsAction(BaseModel):
  def __init__(self):
    pass

class CollectionAnalysis(BaseModel):
  def __init__(self):
    pass

class Methods(BaseModel):
  def __init__(self):
    pass

class AccreditedDataAnalysis(BaseModel):
  def __init__(self):
    pass


