import lirc
import logging
import time
import timeit

class Race:

    DELAY = 0.009
    WRITE_TIMEOUT = 0.028
    READ_TIMEOUT = 0.75

    def __init__(self):
        self.remote = "carrera"
        self.conn = None
        self.socket = "/usr/local/var/run/lirc/lircd"

    def __lirc_conn(self):
        return lirc.CommandConnection(socket_path=self.socket)

    def __find_sync(self):
        """Waits for a blast from the lirc process and returns true if it's
           a syncing signal from the Carrera IR tower."""
        sync = "SYNC %s" % self.remote

        try:
            msg = self.conn.readline(Race.READ_TIMEOUT)
            return sync in msg
        except Exception as e:
            logging.warn("Did not receive SYNC from %s, skipping." % self.remote)
            return False


    def __send(self, cmd):
        """Attempt to send command to lirc via the socket."""
        try:
            lirc.SendCommand(self.conn, self.remote, [cmd]).run(Race.WRITE_TIMEOUT)
        except lirc.client.TimeoutException:
            logging.warn("Player %d send_on__sendce to lirc timed out" % p.nth)
        except BrokenPipeError:
            logging.info("Refreshing lirc connection")
            self.conn.close()
            self.conn = self.__lirc_conn()


    def run(self):
        try:
            self.conn = self.__lirc_conn();

            while True:
                if self.__find_sync():

                    self.__send("P0S3L0")
                    self.__send("P1S3L0")
                    self.__send("P2S3L0")
                    self.__send("P3S3L0")

        except KeyboardInterrupt:
            logging.warn("Terminating Race")
        finally:
            if self.conn:
                self.conn.close()


if __name__ == '__main__':

    r = Race()
    r.run()
