package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.Timer;

public class TimerEvent extends Event {
    private Timer timer;
    public TimerEvent(double time, Timer timer) {
        super(time);
        this.timer = timer;
    }
    @Override
    public boolean isValid() {
        return timer.isValid();
    }

    @Override
    public boolean finished() {
        return true;
    }
}
