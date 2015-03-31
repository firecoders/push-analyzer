class Signal:
    def __init__ ( self ):
        self.subscribers = []

    def subscribe ( self, subscriber ):
        self.subscribers.append ( subscriber )

    def unsubscribe ( self, subscriber ):
        self.subscribers.remove ( subscriber )

    def __call__ ( self, *args, **kwargs ):
        for subscriber in self.subscribers:
            subscriber ( *args, **kwargs )
