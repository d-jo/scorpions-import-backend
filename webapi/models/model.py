
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
  __slots__ = [
    'id',
    'description',
    'bloom',
    'common_graduate_program_slo'
  ]
  def __init__(self):
    pass

class Measure(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'title',
    'description',
    'domain',
    'type',
    'point_in_program',
    'population_measured',
    'frequency_of_collection',
    'proficiency_threshold',
    'proficiency_target'
  ]
  def __init__(self):
    pass

class DecisionsAction(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'content'
  ]
  def __init__(self):
    pass

class CollectionAnalysis(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'data_collection_date_range',
    'number_of_students_assessed',
    'percentage_who_met_or_exceeded'
  ]
  def __init__(self):
    pass

class Methods(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'measure',
    'domain',
    'data_collection'
  ]
  def __init__(self):
    pass

class AccreditedDataAnalysis(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'status'
  ]
  def __init__(self):
    pass


