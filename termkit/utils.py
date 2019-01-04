class EventHandler:
  def __init__(self):
    self.handlers = {}

  def call(self, type):
    if type in self.handlers:
      for h in self.handlers[type]:
        h()

  def event(self, type):
    def registerhandler(handler):
      if type in self.handlers:
        self.handlers[type].append(handler)
      else:
        self.handlers[type] = [handler]
      return handler
    return registerhandler
