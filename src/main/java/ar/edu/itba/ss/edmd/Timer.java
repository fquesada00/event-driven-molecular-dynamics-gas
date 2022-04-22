package ar.edu.itba.ss.edmd;

public class Timer {
    private boolean isValid;
    public Timer() {
        this.isValid = true;
    }

    public boolean isValid() {
        return isValid;
    }

    public void invalidate(){
        isValid = false;
    }

}
